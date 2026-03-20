from __future__ import annotations

from decimal import Decimal, InvalidOperation
import re


def to_decimal(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _avg(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal("0")
    return sum(values) / Decimal(len(values))


def _candidate_gszzl(c: dict) -> Decimal:
    m = re.search(r"gszzl=([\-0-9.]+)%", str(c.get("rationale", "")))
    if not m:
        return Decimal("0")
    return to_decimal(m.group(1))


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
    positive_momo = [c for c in candidates if Decimal("0.30") <= _candidate_gszzl(c) <= Decimal("2.40")]
    pullback_momo = [c for c in candidates if Decimal("-3.50") <= _candidate_gszzl(c) <= Decimal("-0.80")]
    strong_switch_count = len([c for c in positive_momo if to_decimal(c.get("confidence", "0")) >= Decimal("0.78")])

    # momentum score: emphasize top confidence + presence of tradeable trend continuation names.
    refined_count = Decimal(str(len(candidates)))
    depth_factor = min(refined_count / Decimal("12"), Decimal("1"))
    trend_bonus = Decimal(min(strong_switch_count, 3)) * Decimal("6")
    pullback_bonus = Decimal(min(len(pullback_momo), 3)) * Decimal("3")
    momentum_score = (avg_conf * Decimal("55") + top3_conf * Decimal("45")) * depth_factor + trend_bonus + pullback_bonus
    momentum_threshold = Decimal("72")
    momentum_pass = momentum_score >= momentum_threshold

    # drawdown gate: read threshold from strategy_mode.json (default -5.00% for aggressive_short_term)
    drawdown_cfg = hard.get("drawdownGate", {}) if isinstance(hard, dict) else {}
    drawdown_threshold_str = str(drawdown_cfg.get("currentThreshold", "-5.00%")).replace("%", "")
    drawdown_threshold_pct = to_decimal(drawdown_threshold_str, "-5.00")
    drawdown_pass = drawdown_pct >= drawdown_threshold_pct

    # tiered response: reduce buy size at -3%, hard stop at -5%, emergency pause at -8%
    tiered_response = drawdown_cfg.get("tieredResponse", {}) if isinstance(drawdown_cfg, dict) else {}
    drawdown_tier = "normal"
    drawdown_size_multiplier = Decimal("1.0")
    if drawdown_pct <= Decimal("-8.00"):
        drawdown_tier = "emergency_pause"
        drawdown_size_multiplier = Decimal("0.0")
    elif drawdown_pct <= Decimal("-5.00"):
        drawdown_tier = "hard_stop"
        drawdown_size_multiplier = Decimal("0.0")
    elif drawdown_pct <= Decimal("-3.00"):
        drawdown_tier = "reduce_size"
        drawdown_size_multiplier = Decimal("0.5")

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

    strong_switch_ready = strong_switch_count >= 1 and top3_conf >= Decimal("0.78")

    # risk switch computed from pnl + gate status
    if total_upnl < 0 and not momentum_pass and not strong_switch_ready:
        risk_switch = "risk_off"
    elif (momentum_pass and drawdown_pass) or strong_switch_ready:
        risk_switch = "risk_on"
    else:
        risk_switch = "neutral"

    passes = sum([1 if momentum_pass else 0, 1 if drawdown_pass else 0, 1 if oversold_pass else 0])
    consistent = (passes >= 2 and risk_switch != "risk_off") or strong_switch_ready

    confidence_tier = "C"
    suggested_buy_pct = Decimal("0.05")
    if strong_switch_ready and drawdown_pass:
        confidence_tier = "A"
        suggested_buy_pct = Decimal("0.12")
    elif consistent and top3_conf >= Decimal("0.76"):
        confidence_tier = "B"
        suggested_buy_pct = Decimal("0.08")
    elif consistent:
        confidence_tier = "C"
        suggested_buy_pct = Decimal("0.05")

    adjusted_buy_pct = (suggested_buy_pct * drawdown_size_multiplier).quantize(Decimal("0.01"))

    # exit consensus: allow faster risk-reduction when trend/risk degrades.
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
            "strongSwitchCount": strong_switch_count,
            "pullbackCount": len(pullback_momo),
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
            "tier": drawdown_tier,
            "sizeMultiplier": f"{drawdown_size_multiplier:.2f}",
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
            "rule": "Need >=2/3 gates pass and riskSwitchComputed != risk_off, or qualify via strong-switch channel",
            "confidenceTier": confidence_tier,
            "suggestedBuyPct": f"{suggested_buy_pct:.2f}",
            "adjustedSuggestedBuyPct": f"{adjusted_buy_pct:.2f}",
            "strongSwitchReady": strong_switch_ready,
        },
        "exitConsensus": {
            "allowed": exit_allowed,
            "actionHint": "REDEEM_REDUCE_ALLOWED" if exit_allowed else "HOLD",
            "rule": "riskSwitchComputed == risk_off and (passes<=1 or drawdownPct<=-1.00)",
        },
    }
