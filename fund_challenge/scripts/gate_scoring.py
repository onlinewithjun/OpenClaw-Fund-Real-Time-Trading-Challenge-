from __future__ import annotations

from decimal import Decimal, InvalidOperation


def to_decimal(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _avg(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0")
    return sum(values) / Decimal(len(values))


def compute_gate_scoring(state: dict, strategy_mode: dict | None, candidates_json: dict | None) -> dict:
    strategy_mode = strategy_mode or {}
    hard = strategy_mode.get("hardGuards", {}) if isinstance(strategy_mode, dict) else {}
    oversold_cfg = strategy_mode.get("oversoldRotationChannel", {}) if isinstance(strategy_mode, dict) else {}

    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    portfolio_value = to_decimal(state.get("cash", "0"))
    total_upnl = Decimal("0")
    gainers = 0
    losers = 0

    for h in holdings:
        mv = to_decimal(h.get("marketValue", "0"))
        upnl = to_decimal(h.get("unrealizedPnl", "0"))
        portfolio_value += mv
        total_upnl += upnl
        if upnl > 0:
            gainers += 1
        elif upnl < 0:
            losers += 1

    drawdown_pct = Decimal("0")
    if portfolio_value > 0:
        drawdown_pct = (total_upnl / portfolio_value) * Decimal("100")

    candidates = []
    if isinstance(candidates_json, dict):
        candidates = candidates_json.get("candidates", []) or []
    confs = [to_decimal(c.get("confidence", "0")) for c in candidates]
    confs_sorted = sorted(confs, reverse=True)
    avg_conf = _avg(confs)
    top3_conf = _avg(confs_sorted[:3])

    # momentum score: emphasize top confidence and depth
    refined_count = Decimal(str(len(candidates)))
    depth_factor = min(refined_count / Decimal("12"), Decimal("1"))  # saturates at 12
    momentum_score = (avg_conf * Decimal("60") + top3_conf * Decimal("40")) * depth_factor
    momentum_threshold = Decimal("78")
    momentum_pass = momentum_score >= momentum_threshold

    # drawdown gate: pass only when drawdown not too deep
    drawdown_threshold_pct = Decimal("-1.50")
    drawdown_pass = drawdown_pct >= drawdown_threshold_pct

    # oversold rebound score: requires weakness + defensive/high-confidence candidates
    loser_ratio = Decimal("0")
    total_positions = Decimal(str(max(len(holdings), 1)))
    loser_ratio = Decimal(losers) / total_positions

    defensive_confs = [
        to_decimal(c.get("confidence", "0"))
        for c in candidates
        if str(c.get("category", "")).strip() in {"gold_defensive", "broad_index_core"}
    ]
    defensive_score = _avg(defensive_confs) * Decimal("100")

    oversold_score = loser_ratio * Decimal("40") + max(Decimal("0"), -drawdown_pct) * Decimal("20") + defensive_score * Decimal("0.4")
    oversold_threshold = Decimal("45")
    oversold_pass = oversold_score >= oversold_threshold

    # risk switch computed from pnl + gate status
    if total_upnl < 0 and not momentum_pass:
        risk_switch = "risk_off"
    elif momentum_pass and drawdown_pass:
        risk_switch = "risk_on"
    else:
        risk_switch = "neutral"

    passes = sum([1 if momentum_pass else 0, 1 if drawdown_pass else 0, 1 if oversold_pass else 0])
    consistent = passes >= 2 and risk_switch != "risk_off"

    # exit consensus: allow risk-reduction redemption when trend/risk degrades.
    # This is intentionally conservative: trigger only in risk_off and weak gate context.
    severe_drawdown = drawdown_pct <= Decimal("-1.00")
    weak_gate_context = passes <= 1
    exit_allowed = risk_switch == "risk_off" and (weak_gate_context or severe_drawdown)

    return {
        "riskSwitchComputed": risk_switch,
        "inputs": {
            "portfolioValue": str(portfolio_value),
            "totalUnrealizedPnl": str(total_upnl),
            "drawdownPct": f"{drawdown_pct:.4f}",
            "candidateCount": int(refined_count),
            "avgConfidence": f"{avg_conf:.4f}",
            "top3Confidence": f"{top3_conf:.4f}",
            "losers": losers,
            "gainers": gainers,
        },
        "momentumGate": {
            "enabled": bool((hard.get("momentumGate") or {}).get("enabled", True)),
            "score": f"{momentum_score:.2f}",
            "threshold": str(momentum_threshold),
            "pass": momentum_pass,
        },
        "drawdownGate": {
            "enabled": bool((hard.get("drawdownGate") or {}).get("enabled", True)),
            "drawdownPct": f"{drawdown_pct:.4f}",
            "thresholdPct": str(drawdown_threshold_pct),
            "pass": drawdown_pass,
        },
        "oversoldRotationChannel": {
            "enabled": bool((oversold_cfg or {}).get("enabled", True)),
            "score": f"{oversold_score:.2f}",
            "threshold": str(oversold_threshold),
            "pass": oversold_pass,
        },
        "entryConsensus": {
            "passes": passes,
            "total": 3,
            "consistent": consistent,
            "actionHint": "TRIAL_BUY_ALLOWED" if consistent else "HOLD",
            "rule": "Need >=2/3 gates pass and riskSwitchComputed != risk_off",
        },
        "exitConsensus": {
            "allowed": exit_allowed,
            "actionHint": "REDEEM_REDUCE_ALLOWED" if exit_allowed else "HOLD",
            "rule": "riskSwitchComputed == risk_off and (passes<=1 or drawdownPct<=-1.00)",
        },
    }
