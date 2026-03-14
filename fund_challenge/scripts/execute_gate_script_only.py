from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, time
from decimal import Decimal, InvalidOperation
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
CONSISTENCY_MARKER = WORKSPACE / "fund_challenge" / "runtime" / "consistency_04b.json"
INSTRUMENT_RULES = WORKSPACE / "fund_challenge" / "instrument_rules.json"


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def to_decimal(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def fail(msg: str) -> None:
    print(f"EXECUTE_GATE_ALERT: {msg}")
    raise SystemExit(1)


def ensure_fresh_inputs_today(require_candidates_after: str = "") -> None:
    today = datetime.now().date().isoformat()

    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    as_of = str(state.get("asOf", ""))
    if not as_of or not as_of.startswith(today):
        fail(f"stale_state_asOf {as_of} != {today}")

    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    updated = str(candidates.get("updatedAt", "")) if isinstance(candidates, dict) else ""
    if not updated or not updated.startswith(today):
        fail(f"stale_candidates_updatedAt {updated} != {today}")

    if require_candidates_after:
        try:
            floor_t = datetime.strptime(require_candidates_after, "%H:%M").time()
            updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        except Exception:
            fail(f"bad_candidates_time_check updatedAt={updated} floor={require_candidates_after}")

        if updated_dt.date().isoformat() != today or updated_dt.time() < floor_t:
            fail(f"stale_candidates_window updatedAt={updated} before {require_candidates_after}")


def ensure_consistency_marker(require_consistency_after: str = "") -> None:
    if not require_consistency_after:
        return
    if not CONSISTENCY_MARKER.exists():
        fail(f"missing_consistency_marker {CONSISTENCY_MARKER}")

    marker = load_json(CONSISTENCY_MARKER)
    if marker.get("ok") is not True:
        fail(f"consistency_not_ok reason={marker.get('reason', '')}")

    checked_at = str(marker.get("checkedAt", ""))
    if not checked_at:
        fail("consistency_marker_missing_checkedAt")

    today = datetime.now().date().isoformat()
    try:
        floor_t = datetime.strptime(require_consistency_after, "%H:%M").time()
        checked_dt = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
    except Exception:
        fail(f"bad_consistency_time_check checkedAt={checked_at} floor={require_consistency_after}")

    if checked_dt.date().isoformat() != today or checked_dt.time() < floor_t:
        fail(f"stale_consistency_marker checkedAt={checked_at} before {require_consistency_after}")


def _candidate_gszzl(c: dict) -> float:
    m = re.search(r"gszzl=([\-0-9.]+)%", str(c.get("rationale", "")))
    if not m:
        return 0.0
    try:
        return float(m.group(1))
    except Exception:
        return 0.0


def load_target_remap() -> dict[str, tuple[str, str]]:
    try:
        rules = load_json(INSTRUMENT_RULES)
        remap = rules.get("targetRemap", {}) if isinstance(rules, dict) else {}
        out: dict[str, tuple[str, str]] = {}
        for src, dst in remap.items():
            if not isinstance(dst, dict):
                continue
            code = str(dst.get("code", "")).strip()
            name = str(dst.get("name", "")).strip()
            if src and code and name:
                out[str(src)] = (code, name)
        return out
    except Exception:
        return {}


def choose_trial_buy_target() -> tuple[str, str] | tuple[None, None]:
    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    if not arr:
        return None, None

    # 短线激进但不追涨：
    # 1) 禁止买入当日过热拉升标的（gszzl >= +2.5%）
    # 2) 优先选择回撤低吸窗口（-3.5% ~ -0.8%）
    eligible = []
    for c in arr:
        gszzl = _candidate_gszzl(c)
        if gszzl >= 2.5:
            continue
        if -3.5 <= gszzl <= -0.8:
            eligible.append(c)

    if not eligible:
        return None, None

    top = sorted(eligible, key=lambda x: float(x.get("confidence", 0)), reverse=True)[0]
    code = str(top.get("code", ""))
    name = str(top.get("name", ""))

    target_remap = load_target_remap()
    if code in target_remap:
        mapped_code, mapped_name = target_remap[code]
        return mapped_code, mapped_name

    return code, name


def compute_trial_amount() -> str:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    cash = to_decimal(state.get("cash", "0"))
    mv = sum(to_decimal(h.get("marketValue", "0")) for h in state.get("holdings", []))
    pv = cash + mv
    amt = (pv * Decimal("0.05")).quantize(Decimal("1"))  # 5% trial
    if amt < Decimal("20"):
        amt = Decimal("20")
    return str(int(amt))


def choose_redeem_target() -> tuple[str, str, str]:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    if not holdings:
        return "020899", "天弘中证全指通信设备指数发起A", "1.00"

    def score(h: dict) -> Decimal:
        mv = to_decimal(h.get("marketValue", "0"))
        upnl = to_decimal(h.get("unrealizedPnl", "0"))
        if mv <= 0:
            return Decimal("999")
        return upnl / mv  # lower is worse

    ranked = sorted(holdings, key=score)
    target = ranked[0]

    cash = to_decimal(state.get("cash", "0"))
    pv = cash + sum(to_decimal(h.get("marketValue", "0")) for h in holdings)
    target_mv = to_decimal(target.get("marketValue", "0"))

    # aggressive profile: redeem ~15% PV, cap at 100% of target holding
    redeem_amt_cny = (pv * Decimal("0.15")).quantize(Decimal("1"))
    cap = (target_mv * Decimal("1.00")).quantize(Decimal("1"))
    if cap > 0 and redeem_amt_cny > cap:
        redeem_amt_cny = cap
    if redeem_amt_cny < Decimal("20"):
        redeem_amt_cny = Decimal("20")

    nav = to_decimal(target.get("latestNav", "0"))
    shares = Decimal("1.00")
    if nav > 0:
        shares = (redeem_amt_cny / nav).quantize(Decimal("0.01"))
        if shares <= 0:
            shares = Decimal("0.01")

    return str(target.get("code", "020899")), str(target.get("name", "天弘中证全指通信设备指数发起A")), f"{shares:.2f}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate executable gate decision with freshness guards")
    ap.add_argument("--require-candidates-after", default="", help="Require daily_candidates.updatedAt >= HH:MM (Asia/Shanghai)")
    ap.add_argument("--require-consistency-after", default="", help="Require 04b consistency marker checkedAt >= HH:MM (Asia/Shanghai)")
    args = ap.parse_args()

    ensure_fresh_inputs_today(require_candidates_after=args.require_candidates_after)
    ensure_consistency_marker(require_consistency_after=args.require_consistency_after)

    # 1) Build/validate evidence with gate scoring
    code, out, err = run([
        sys.executable,
        "fund_challenge/scripts/preflight_guard.py",
        "--phase",
        "EXECUTE_READY",
        "--workspace",
        ".",
        "--with-publish-gate",
        "--compact",
    ])
    if code != 0:
        fail(f"preflight_failed {err[:120]}")

    evidence = load_json(WORKSPACE / "fund_challenge" / "evidence" / "latest.json")
    gs = evidence.get("gateScoring", {}) if isinstance(evidence, dict) else {}
    entry_hint = ((gs.get("entryConsensus") or {}).get("actionHint") if isinstance(gs, dict) else None) or "HOLD"
    exit_hint = ((gs.get("exitConsensus") or {}).get("actionHint") if isinstance(gs, dict) else None) or "HOLD"

    action = "HOLD"
    reason = "risk_switch_gate"
    code_str = "020899"
    name_str = "天弘中证全指通信设备指数发起A"
    amount = "0"

    # Priority 1: risk reduction when exit consensus triggers.
    if exit_hint == "REDEEM_REDUCE_ALLOWED":
        action = "REDEEM"
        reason = "risk_off_reduce_exposure"
        code_str, name_str, amount = choose_redeem_target()
    # Priority 2: trial buy when entry consensus allows and cash is sufficient.
    elif entry_hint == "TRIAL_BUY_ALLOWED":
        trial_amount = compute_trial_amount()
        state = load_json(WORKSPACE / "fund_challenge" / "state.json")
        cash = to_decimal(state.get("cash", "0"))
        if cash >= to_decimal(trial_amount):
            buy_code, buy_name = choose_trial_buy_target()
            if buy_code and buy_name:
                action = "BUY"
                reason = "gate_consensus_trial_buy_pullback_only"
                code_str, name_str = buy_code, buy_name
                amount = trial_amount
            else:
                action = "HOLD"
                reason = "no_pullback_entry_or_overheat_filtered"
                amount = "0"
        else:
            # No cash available: generate executable reduce signal instead of impossible buy.
            action = "REDEEM"
            reason = "raise_cash_for_next_trial_buy"
            code_str, name_str, amount = choose_redeem_target()

    # 2) Build decision packet and short line
    code2, out2, err2 = run([
        sys.executable,
        "fund_challenge/scripts/run_decision_pipeline.py",
        "--phase",
        "EXECUTE_READY",
        "--workspace",
        ".",
        "--action",
        action,
        "--code",
        code_str,
        "--name",
        name_str,
        "--amount-cny",
        amount,
        "--reason",
        reason,
        "--deadline",
        "15:00 Asia/Shanghai",
        "--fallback",
        "HOLD",
    ])
    if code2 != 0:
        fail(f"pipeline_failed {err2[:120]}")

    short_file = WORKSPACE / "fund_challenge" / "out" / "decision.short.txt"
    if short_file.exists():
        print(short_file.read_text(encoding="utf-8").strip())
        return

    print("EXECUTE_GATE_ALERT: missing decision.short.txt")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
