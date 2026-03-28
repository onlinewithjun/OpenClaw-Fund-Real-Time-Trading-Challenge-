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
PULLBACK_MIN_GSZZL = -3.5
PULLBACK_MAX_GSZZL = -0.8
ALIPAY_ALLOWED = WORKSPACE / "fund_challenge" / "universe" / "alipay_allowed.json"


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


def _candidate_total_score(c: dict) -> float:
    m = re.search(r"score=([\-0-9.]+)", str(c.get("rationale", "")))
    if not m:
        return 0.0
    try:
        return float(m.group(1))
    except Exception:
        return 0.0


def load_alipay_allowed_codes() -> set[str]:
    if not ALIPAY_ALLOWED.exists():
        return set()
    try:
        data = load_json(ALIPAY_ALLOWED)
    except Exception:
        return set()
    allowed = data.get("allowed", []) if isinstance(data, dict) else []
    return {
        str(item.get("code", "")).strip()
        for item in allowed
        if isinstance(item, dict) and str(item.get("code", "")).strip()
    }


def recent_redeem_codes(days: int = 5) -> set[str]:
    ledger = WORKSPACE / "fund_challenge" / "ledger.jsonl"
    if not ledger.exists():
        return set()
    cutoff = datetime.now().timestamp() - days * 86400
    out: set[str] = set()
    try:
        for raw in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.replace("\x00", "").strip()
            if not line.startswith("{"):
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
            if str(item.get("event", "")) != "execution_confirmed":
                continue
            if str(item.get("actionType", "")).upper() != "REDEEM":
                continue
            ts = str(item.get("ts", "")).replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(ts)
            except Exception:
                continue
            if dt.timestamp() < cutoff:
                continue
            note = str(item.get("note", ""))
            code = str(item.get("code", "")).strip()
            if code:
                out.add(code)
                continue
            m = re.search(r"sold\s+(\d{6})", note)
            if m:
                out.add(m.group(1))
    except Exception:
        return set()
    return out


def recent_redeem_map(days: int = 7) -> dict[str, datetime]:
    ledger = WORKSPACE / "fund_challenge" / "ledger.jsonl"
    if not ledger.exists():
        return {}
    cutoff = datetime.now().timestamp() - days * 86400
    out: dict[str, datetime] = {}
    try:
        for raw in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.replace("\x00", "").strip()
            if not line.startswith("{"):
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
            if str(item.get("event", "")) != "execution_confirmed":
                continue
            if str(item.get("actionType", "")).upper() != "REDEEM":
                continue
            ts = str(item.get("ts", "")).replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(ts)
            except Exception:
                continue
            if dt.timestamp() < cutoff:
                continue
            code = str(item.get("code", "")).strip()
            if not code:
                note = str(item.get("note", ""))
                m = re.search(r"sold\s+(\d{6})", note)
                if m:
                    code = m.group(1)
            if not code:
                continue
            prev = out.get(code)
            if prev is None or dt > prev:
                out[code] = dt
    except Exception:
        return {}
    return out


def _normalize_share_class_name(name: str) -> str:
    s = str(name or "").strip().lower()
    s = s.replace("（", "(").replace("）", ")")
    s = re.sub(r"\s+[acihe]$", "", s)
    return s


def _dedupe_share_classes(candidates: list[dict], holding_codes: set[str]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for c in candidates:
        key = _normalize_share_class_name(str(c.get("name", ""))) or str(c.get("code", ""))
        current = grouped.get(key)
        if current is None:
            grouped[key] = c
            continue
        cur_code = str(current.get("code", "")).strip()
        new_code = str(c.get("code", "")).strip()
        cur_conf = float(current.get("confidence", 0) or 0)
        new_conf = float(c.get("confidence", 0) or 0)
        cur_momo = _candidate_gszzl(current)
        new_momo = _candidate_gszzl(c)
        if new_code in holding_codes and cur_code not in holding_codes:
            grouped[key] = c
            continue
        if (new_conf, new_momo) > (cur_conf, cur_momo):
            grouped[key] = c
    return list(grouped.values())


def portfolio_context() -> tuple[dict[str, Decimal], dict[str, Decimal], Decimal]:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    category_map = {str(c.get("code", "")).strip(): str(c.get("category", "")).strip() for c in arr}

    cash = to_decimal(state.get("cash", "0"))
    holding_mv = sum(to_decimal(h.get("marketValue", "0")) for h in holdings)
    pv = cash + holding_mv

    holding_weights: dict[str, Decimal] = {}
    category_weights: dict[str, Decimal] = {}
    for h in holdings:
        code = str(h.get("code", "")).strip()
        mv = to_decimal(h.get("marketValue", "0"))
        if not code or pv <= Decimal("0"):
            continue
        w = mv / pv
        holding_weights[code] = w
        category = category_map.get(code, "")
        if category:
            category_weights[category] = category_weights.get(category, Decimal("0")) + w
    return holding_weights, category_weights, pv


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


def active_pending_transactions() -> list[dict]:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
    out = []
    for t in pending:
        if str(t.get("status", "")).upper() in {"SETTLED", "CANCELLED", "FAILED"}:
            continue
        if str(t.get("resolvedAt", "")).strip():
            continue
        out.append(t)
    return out


def pending_blocker_summary(active_pending: list[dict], *, blocking_count: int | None = None, label: str = "pending_transactions_block_new_signal") -> str:
    if not active_pending:
        return ""

    today = datetime.now().date()
    oldest = ""
    overnight_codes: list[str] = []
    for t in active_pending:
        created_at = str((t or {}).get("createdAt", "")).strip()
        code = str((t or {}).get("code", "")).strip()
        if not created_at:
            continue
        try:
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except Exception:
            continue
        if not oldest or created_at < oldest:
            oldest = created_at
        if created_dt.date() < today and code:
            overnight_codes.append(code)

    overnight_codes = sorted(set(overnight_codes))
    overnight_part = f"_overnight_{len(overnight_codes)}" if overnight_codes else ""
    oldest_part = f"_oldest_{oldest[:10].replace('-', '')}" if oldest else ""
    count = blocking_count if blocking_count is not None else len(active_pending)
    return f"{label}_{count}{overnight_part}{oldest_part}"


def classify_pending_constraints(active_pending: list[dict], intended_action: str = "", intended_buy_amount: Decimal | None = None) -> tuple[bool, str]:
    """
    Classify pending transaction constraints.
    
    Key rules:
    - Same-code pending BUY/REDEEM blocks new action on that code
    - Insufficient cash blocks new BUY (considering intended_buy_amount)
    - Overnight pending BUY does NOT block different-code actions if cash is sufficient
    """
    if not active_pending:
        return False, ""

    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    cash = to_decimal(state.get("cash", "0"))

    same_code_pending = []
    for t in active_pending:
        action_type = str((t or {}).get("actionType", "")).upper()
        code = str((t or {}).get("code", "")).strip()
        if intended_action and code and code == intended_action:
            same_code_pending.append(t)

    # Same-code pending is always a blocker
    if same_code_pending:
        return True, pending_blocker_summary(same_code_pending, label="same_code_pending_blocks_new_signal")

    # Check cash sufficiency for intended BUY
    if intended_buy_amount is not None and intended_buy_amount > Decimal("0"):
        if cash < intended_buy_amount:
            return True, f"insufficient_cash_for_buy need={intended_buy_amount} have={cash}"

    # Redeem-in-flight is informative, not a hard blocker, as long as current liquid cash can support a new buy.
    if cash <= Decimal("0"):
        return True, pending_blocker_summary(active_pending, label="no_cash_with_pending_redeem")

    return False, pending_blocker_summary(active_pending, blocking_count=0, label="pending_non_blocking")


def classify_candidate_context(c: dict, *, candidate_count: int, top_gszzl: float, holding_codes: set[str], recent_redeem_times: dict[str, datetime], holding_weights: dict[str, Decimal], category_weights: dict[str, Decimal]) -> tuple[str, str]:
    code = str(c.get("code", "")).strip()
    gszzl = _candidate_gszzl(c)
    conf = float(c.get("confidence", 0) or 0)
    category = str(c.get("category", "")).strip()
    rationale = str(c.get("rationale", ""))
    persistence = 1 if "persistence=1" in rationale else 0
    today = datetime.now().date()

    recent_redeem_dt = recent_redeem_times.get(code)
    if recent_redeem_dt is not None:
        days_since = (today - recent_redeem_dt.date()).days
        if days_since <= 1:
            return "reject", "low_quality_rebuy_recent_redeem"

    holding_weight = holding_weights.get(code, Decimal("0"))
    category_weight = category_weights.get(category, Decimal("0"))
    if code in holding_codes and holding_weight >= Decimal("0.30"):
        return "reject", "single_name_already_too_large"
    if category and category_weight >= Decimal("0.45"):
        return "reject", "category_already_too_large"

    # 回撤低吸：优先处理可解释的温和回撤，而不是追强。
    if PULLBACK_MIN_GSZZL <= gszzl <= PULLBACK_MAX_GSZZL and conf >= 0.70:
        if persistence >= 1:
            return "pullback", "washout_pullback_with_persistence"
        return "pullback", "washout_pullback"

    # 对日内强势做语境判断，而不是死阈值。
    leader_gap = top_gszzl - gszzl
    is_leader = leader_gap <= 0.35
    crowded_up = gszzl >= 3.0 and conf < 0.88
    sharp_pop_existing = code in holding_codes and gszzl >= 1.2 and persistence == 1
    hot_newcomer = persistence == 0 and gszzl >= 2.0 and conf < 0.86 and candidate_count >= 6
    defensive_ok = category == "gold_defensive" and persistence == 1 and gszzl <= 1.2

    if sharp_pop_existing:
        return "reject", "overextended_existing_holding"
    if crowded_up and is_leader:
        return "reject", "overextended_up_leader"
    if hot_newcomer:
        return "reject", "hot_newcomer_without_confirmation"

    # 允许的趋势延续：不是领涨过热、不是刚卖又追回、并且有一定延续证据。
    if 0.2 <= gszzl <= 2.2 and conf >= 0.82:
        if defensive_ok:
            return "strong_switch", "defensive_trend_continuation"
        if persistence >= 1 or leader_gap >= 0.4:
            return "strong_switch", "trend_continuation_not_overextended"

    return "reject", "no_fresh_edge"


def choose_trial_buy_target() -> tuple[str, str, str] | tuple[None, None, None]:
    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    if not arr:
        return None, None, None

    allowed_codes = load_alipay_allowed_codes()
    if allowed_codes:
        arr = [c for c in arr if str(c.get("code", "")).strip() in allowed_codes]
    if not arr:
        return None, None, None

    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    holding_codes = {str(h.get("code", "")).strip() for h in state.get("holdings", []) if str(h.get("code", "")).strip()}
    arr = _dedupe_share_classes(arr, holding_codes)
    recent_redeem_times = recent_redeem_map(days=7)
    holding_weights, category_weights, _pv = portfolio_context()
    top_gszzl = max((_candidate_gszzl(c) for c in arr), default=0.0)

    pullback: list[dict] = []
    strong_switch: list[dict] = []
    for c in arr:
        lane, _reason = classify_candidate_context(
            c,
            candidate_count=len(arr),
            top_gszzl=top_gszzl,
            holding_codes=holding_codes,
            recent_redeem_times=recent_redeem_times,
            holding_weights=holding_weights,
            category_weights=category_weights,
        )
        if lane == "pullback":
            pullback.append(c)
        elif lane == "strong_switch":
            strong_switch.append(c)

    lane = None
    eligible = []
    def rank_pullback(x: dict) -> tuple[float, float, int, float]:
        code = str(x.get("code", "")).strip()
        return (
            _candidate_total_score(x),
            float(x.get("confidence", 0) or 0),
            0 if code in holding_codes else 1,
            -abs(_candidate_gszzl(x) + 1.5),
        )

    def rank_strong_switch(x: dict) -> tuple[float, int, float, float]:
        code = str(x.get("code", "")).strip()
        return (
            _candidate_total_score(x),
            0 if code in holding_codes else 1,
            float(x.get("confidence", 0) or 0),
            _candidate_gszzl(x),
        )

    if pullback:
        lane = "pullback"
        eligible = sorted(pullback, key=rank_pullback, reverse=True)
    elif strong_switch:
        lane = "strong_switch"
        eligible = sorted(strong_switch, key=rank_strong_switch, reverse=True)

    if not eligible:
        return None, None, None

    top = eligible[0]
    code = str(top.get("code", ""))
    name = str(top.get("name", ""))

    target_remap = load_target_remap()
    if code in target_remap:
        mapped_code, mapped_name = target_remap[code]
        return mapped_code, mapped_name, lane or "pullback"

    return code, name, lane or "pullback"


def compute_trial_amount(gs: dict) -> str:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    cash = to_decimal(state.get("cash", "0"))
    mv = sum(to_decimal(h.get("marketValue", "0")) for h in state.get("holdings", []))
    pv = cash + mv
    entry = (gs.get("entryConsensus") or {}) if isinstance(gs, dict) else {}
    buy_pct = to_decimal(entry.get("adjustedSuggestedBuyPct", entry.get("suggestedBuyPct", "0.05")), "0.05")

    # Respect drawdown-tier sizing from gate_scoring.
    # 0.00 means hard stop / emergency pause and must not be floored back to a live trial buy.
    if buy_pct <= Decimal("0"):
        return "0"

    if buy_pct < Decimal("0.05"):
        buy_pct = Decimal("0.05")
    amt = (pv * buy_pct).quantize(Decimal("1"))
    if amt < Decimal("20"):
        amt = Decimal("20")
    return str(int(amt))


def choose_redeem_target() -> tuple[str, str, str]:
    state = load_json(WORKSPACE / "fund_challenge" / "state.json")
    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    if not holdings:
        return "020899", "天弘中证全指通信设备指数发起A", "1.00"

    pending_codes = {
        str(t.get("code", "")).strip()
        for t in active_pending_transactions()
        if str(t.get("code", "")).strip()
    }

    candidates = load_json(WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json")
    arr = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    candidate_map = {str(c.get('code', '')): c for c in arr if str(c.get('code', '')).strip()}

    def failure_score(h: dict) -> Decimal:
        code = str(h.get("code", "")).strip()
        mv = to_decimal(h.get("marketValue", "0"))
        upnl = to_decimal(h.get("unrealizedPnl", "0"))
        rel = Decimal("0")
        if mv > 0:
            rel = upnl / mv

        c = candidate_map.get(code)
        conf_penalty = Decimal("0.20")
        momo_penalty = Decimal("0.20")
        absent_penalty = Decimal("0.35")
        if c:
            conf_penalty = Decimal("1") - to_decimal(c.get("confidence", "0"), "0")
            momo_penalty = max(Decimal("0"), Decimal("0.8") - to_decimal(str(_candidate_gszzl(c)), "0") / Decimal("10"))
            absent_penalty = Decimal("0")
        return rel - conf_penalty - momo_penalty - absent_penalty

    eligible_holdings = [h for h in holdings if str(h.get("code", "")).strip() not in pending_codes]
    ranked = sorted((eligible_holdings or holdings), key=failure_score)
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
    entry = (gs.get("entryConsensus") or {}) if isinstance(gs, dict) else {}
    entry_hint = (entry.get("actionHint") if isinstance(entry, dict) else None) or "HOLD"
    exit_hint = ((gs.get("exitConsensus") or {}).get("actionHint") if isinstance(gs, dict) else None) or "HOLD"
    tier = str(entry.get("confidenceTier", "C"))

    action = "HOLD"
    reason = "risk_switch_gate"
    code_str = "020899"
    name_str = "天弘中证全指通信设备指数发起A"
    amount = "0"

    active_pending = active_pending_transactions()
    # Priority 1: risk reduction when exit consensus triggers.
    if exit_hint == "REDEEM_REDUCE_ALLOWED":
        blocked, block_reason = classify_pending_constraints(active_pending)
        if blocked:
            action = "HOLD"
            reason = block_reason
        else:
            action = "REDEEM"
            reason = "risk_off_reduce_exposure"
            code_str, name_str, amount = choose_redeem_target()
    # Priority 2: trial buy when entry consensus allows and cash is sufficient.
    elif entry_hint == "TRIAL_BUY_ALLOWED":
        trial_amount = compute_trial_amount(gs)
        state = load_json(WORKSPACE / "fund_challenge" / "state.json")
        cash = to_decimal(state.get("cash", "0"))
        trial_amount_decimal = to_decimal(trial_amount)
        if trial_amount_decimal <= Decimal("0"):
            action = "HOLD"
            reason = "drawdown_tier_blocks_trial_buy"
            amount = "0"
        else:
            buy_code, buy_name, lane = choose_trial_buy_target()
            blocked, block_reason = classify_pending_constraints(active_pending, intended_action=buy_code or "", intended_buy_amount=trial_amount_decimal)
            if blocked:
                action = "HOLD"
                reason = block_reason
                amount = "0"
            elif cash >= trial_amount_decimal:
                if buy_code and buy_name:
                    action = "BUY"
                    reason = f"gate_consensus_{(lane or 'pullback')}_tier_{tier.lower()}"
                    code_str, name_str = buy_code, buy_name
                    amount = trial_amount
                else:
                    action = "HOLD"
                    reason = "no_valid_entry_after_pullback_and_strong_switch_filters"
                    amount = "0"
            else:
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
