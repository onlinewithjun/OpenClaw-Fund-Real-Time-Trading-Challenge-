from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def to_decimal(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def score(state: dict, strategy_mode: dict, candidates: dict) -> dict:
    holdings = state.get("holdings", [])
    mv = sum(to_decimal(h.get("marketValue", "0")) for h in holdings)
    upnl = sum(to_decimal(h.get("unrealizedPnl", "0")) for h in holdings)
    gains = sum(1 for h in holdings if to_decimal(h.get("unrealizedPnl", "0")) > 0)
    losses = sum(1 for h in holdings if to_decimal(h.get("unrealizedPnl", "0")) < 0)
    pnl_ratio = (upnl / mv) if mv > 0 else Decimal("0")

    # risk switch (quantized, not prompt-only)
    if pnl_ratio <= Decimal("-0.010") or (losses >= 2 and gains == 0):
        risk_switch = "risk_off"
    elif pnl_ratio >= Decimal("0.005") and gains >= losses:
        risk_switch = "risk_on"
    else:
        risk_switch = "neutral"

    cands = candidates.get("candidates", []) if isinstance(candidates, dict) else []
    confs = []
    for c in cands:
        try:
            confs.append(float(c.get("confidence", 0)))
        except Exception:
            continue
    confs_sorted = sorted(confs, reverse=True)
    top5 = confs_sorted[:5]
    avg_top5 = (sum(top5) / len(top5)) if top5 else 0.0
    high_conf_ratio = (sum(1 for x in top5 if x >= 0.85) / len(top5)) if top5 else 0.0

    momentum_score = round(avg_top5 * 100, 2)
    momentum_pass = bool(top5) and avg_top5 >= 0.86 and high_conf_ratio >= 0.6 and risk_switch != "risk_off"

    target = to_decimal((state.get("challenge") or {}).get("targetValue", "2000"), "2000")
    pv = to_decimal(state.get("portfolioValue", "0"), "0")
    distance_ratio = ((target - pv) / target) if target > 0 else Decimal("1")
    drawdown = (-upnl / mv) if mv > 0 and upnl < 0 else Decimal("0")

    # stricter drawdown gate: fail when drawdown too high in short-term mode
    drawdown_threshold = Decimal("0.015")  # 1.5%
    drawdown_score = float(max(Decimal("0"), Decimal("100") - (drawdown * Decimal("5000"))))
    drawdown_pass = drawdown <= drawdown_threshold

    cyc_or_tech_high = any(
        (str(c.get("category", "")) in {"cyclical_resources", "tech_growth"}) and float(c.get("confidence", 0)) >= 0.88
        for c in cands
    ) if cands else False

    oversold_score = round((60 if cyc_or_tech_high else 25) + (20 if drawdown_pass else 0) + (20 if risk_switch != "risk_off" else 0), 2)
    oversold_pass = cyc_or_tech_high and drawdown_pass and risk_switch != "risk_off"

    pass_count = sum([1 if momentum_pass else 0, 1 if drawdown_pass else 0, 1 if oversold_pass else 0])
    consensus_pass = (pass_count >= 2) and risk_switch != "risk_off"

    return {
        "riskSwitch": {
            "computed": risk_switch,
            "pnlRatio": float(pnl_ratio),
            "gainers": gains,
            "losers": losses,
            "rule": "pnl_ratio + gain/loss breadth",
        },
        "momentumGate": {
            "score": momentum_score,
            "pass": momentum_pass,
            "avgTop5Confidence": round(avg_top5, 4),
            "highConfRatioTop5": round(high_conf_ratio, 4),
        },
        "drawdownGate": {
            "score": round(drawdown_score, 2),
            "pass": drawdown_pass,
            "drawdown": float(drawdown),
            "threshold": float(drawdown_threshold),
            "distanceToTargetRatio": float(distance_ratio),
        },
        "oversoldRotationChannel": {
            "score": oversold_score,
            "pass": oversold_pass,
            "hasHighConfCyclicalOrTech": bool(cyc_or_tech_high),
        },
        "consensus": {
            "pass": consensus_pass,
            "passedGates": pass_count,
            "required": 2,
            "reason": "risk_off blocks new risk" if risk_switch == "risk_off" else ""
        },
        "meta": {
            "mode": strategy_mode.get("mode", "unknown"),
            "candidateCount": len(cands),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Quantized gate scoring for challenge decisions")
    ap.add_argument("--state", required=True)
    ap.add_argument("--strategy", default="fund_challenge/universe/strategy_mode.json")
    ap.add_argument("--candidates", default="fund_challenge/universe/daily_candidates.json")
    args = ap.parse_args()

    state = load_json(Path(args.state))
    strategy = load_json(Path(args.strategy)) if Path(args.strategy).exists() else {}
    candidates = load_json(Path(args.candidates)) if Path(args.candidates).exists() else {}

    print(json.dumps(score(state, strategy, candidates), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
