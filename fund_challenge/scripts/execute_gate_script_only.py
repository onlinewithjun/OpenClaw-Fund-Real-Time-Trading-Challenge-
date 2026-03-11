from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]


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


def ensure_fresh_inputs_today() -> None:
    today = datetime.now().date().isoformat()

    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    as_of = str(state.get("asOf", ""))
    if not as_of or not as_of.startswith(today):
        fail(f"stale_state_asOf {as_of} != {today}")

    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    updated = str(candidates.get("updatedAt", "")) if isinstance(candidates, dict) else ""
    if not updated or not updated.startswith(today):
        fail(f"stale_candidates_updatedAt {updated} != {today}")


def choose_trial_buy_target() -> tuple[str, str]:
    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    if not arr:
        return "020899", "天弘中证全指通信设备指数发起A"
    top = sorted(arr, key=lambda x: float(x.get("confidence", 0)), reverse=True)[0]
    return str(top.get("code", "020899")), str(top.get("name", "天弘中证全指通信设备指数发起A"))


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
    ensure_fresh_inputs_today()

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
            action = "BUY"
            reason = "gate_consensus_trial_buy"
            code_str, name_str = choose_trial_buy_target()
            amount = trial_amount
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
