from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from gate_scoring import compute_gate_scoring
from state_math import compute


def now_zh_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def _compute_candidate_score(c: dict) -> dict:
    """
    Transparent multi-factor scoring for individual candidates.
    
    Formula:
      score = momentum_component * 0.40 + stability * 0.25 + confidence * 0.20 + diversity * 0.15
    
    Returns breakdown for auditability.
    """
    rationale = str(c.get("rationale", ""))
    
    # Extract gszzl (estimated daily return)
    gszzl_match = re.search(r"gszzl=([\-0-9.]+)%", rationale)
    gszzl = Decimal(gszzl_match.group(1)) if gszzl_match else Decimal("0")
    
    # Extract stability (0-1 scale)
    stability_match = re.search(r"stability=([0-9.]+)", rationale)
    stability = Decimal(stability_match.group(1)) if stability_match else Decimal("0")
    
    # Extract confidence (0-1 scale)
    confidence = Decimal(str(c.get("confidence", "0")))
    
    # Momentum z-score approximation (map gszzl to z-score)
    # Assume normal distribution with mean=1.5%, std=2.0%
    momentum_mean = Decimal("1.5")
    momentum_std = Decimal("2.0")
    momentum_z = (gszzl - momentum_mean) / momentum_std
    momentum_z_clamped = max(Decimal("-2"), min(Decimal("2"), momentum_z))  # Clamp to [-2, 2]
    momentum_component = ((momentum_z_clamped + Decimal("2")) / Decimal("4")) * Decimal("100")  # Normalize to 0-100
    
    # Stability component (already 0-1, scale to 0-100)
    stability_component = stability * Decimal("100")
    
    # Confidence component (already 0-1, scale to 0-100)
    confidence_component = confidence * Decimal("100")
    
    # Diversity bonus: penalize overcrowded sectors
    category = str(c.get("category", ""))
    sector_overcrowding_penalty = Decimal("0")
    if "tech" in category.lower() or "growth" in category.lower():
        sector_overcrowding_penalty = Decimal("10")  # Tech sectors tend to be crowded
    
    diversity_component = max(Decimal("0"), Decimal("100") - sector_overcrowding_penalty)
    
    # Weighted final score
    score = (
        momentum_component * Decimal("0.40") +
        stability_component * Decimal("0.25") +
        confidence_component * Decimal("0.20") +
        diversity_component * Decimal("0.15")
    )
    
    return {
        "score": float(score.quantize(Decimal("0.01"))),
        "factors": {
            "momentum_z": float(momentum_z_clamped),
            "momentum_component": float(momentum_component.quantize(Decimal("0.01"))),
            "gszzl": float(gszzl),
            "stability": float(stability),
            "stability_component": float(stability_component.quantize(Decimal("0.01"))),
            "confidence": float(confidence),
            "confidence_component": float(confidence_component.quantize(Decimal("0.01"))),
            "diversity_component": float(diversity_component.quantize(Decimal("0.01"))),
            "sector_overcrowding_penalty": float(sector_overcrowding_penalty),
        },
        "weights": {
            "momentum": 0.40,
            "stability": 0.25,
            "confidence": 0.20,
            "diversity": 0.15
        }
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except Exception:
        return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def checksum_state_digest(digest: dict) -> str:
    payload = json.dumps(digest, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def to_decimal(v: object) -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _normalize_fund_name(name: str) -> str:
    s = str(name or "").strip().lower()
    for token in [" ", "（", "）", "(", ")", "联接", "etf", "人民币"]:
        s = s.replace(token, "")
    return s


def _dedupe_share_classes(candidates: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for c in candidates:
        name = str(c.get("name", "")).strip()
        key = re.sub(r"\s+[ACEI]$", "", name.replace("（", "(").replace("）", ")")).lower() or str(c.get("code", ""))
        current = grouped.get(key)
        if current is None:
            grouped[key] = c
            continue
        cur_score = _compute_candidate_score(current)["score"]
        new_score = _compute_candidate_score(c)["score"]
        cur_conf = float(current.get("confidence", 0) or 0)
        new_conf = float(c.get("confidence", 0) or 0)
        if (new_score, new_conf) > (cur_score, cur_conf):
            grouped[key] = c
    return list(grouped.values())


def build_candidate_scoring(candidates: list[dict], generated_at: str) -> dict:
    """Build scored candidate list with factor breakdowns."""
    scored_candidates = []
    for c in _dedupe_share_classes(candidates):
        code = str(c.get("code", "")).strip()
        name = str(c.get("name", "")).strip()
        score_result = _compute_candidate_score(c)
        scored_candidates.append({
            "code": code,
            "name": name,
            "category": c.get("category", ""),
            "score": score_result["score"],
            "factors": score_result["factors"],
            "weights": score_result["weights"],
            "originalConfidence": c.get("confidence", "0"),
            "purchasableOn": c.get("purchasableOn", []),
            "verifiedAt": generated_at,
        })
    
    # Sort by score descending
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Add ranking
    for i, sc in enumerate(scored_candidates):
        sc["rank"] = i + 1
    
    return {
        "scoredCandidates": scored_candidates,
        "count": len(scored_candidates),
        "topScore": scored_candidates[0]["score"] if scored_candidates else 0,
        "avgScore": sum(c["score"] for c in scored_candidates) / len(scored_candidates) if scored_candidates else 0,
        "scoreMethod": "multi_factor_weighted",
        "generatedAt": generated_at,
    }


def build_identity_checks(state: dict, rules: dict, generated_at: str) -> list[dict]:
    funds = (rules.get("funds") or {}) if isinstance(rules, dict) else {}
    checks: list[dict] = []
    for h in state.get("holdings", []):
        code = str(h.get("code", "")).strip()
        name = str(h.get("name", "")).strip()
        rule = funds.get(code, {}) if isinstance(funds, dict) else {}
        rule_name = str(rule.get("name", "")).strip()
        matched = bool(
            code and name and rule_name and (
                name == rule_name or _normalize_fund_name(name) == _normalize_fund_name(rule_name)
            )
        )
        checks.append({
            "code": code,
            "stateName": name,
            "ruleName": rule_name,
            "matched": matched,
            "verifiedAt": generated_at,
            "source": "instrument_rules.json",
        })
    return checks


def build_market_signals(state: dict, generated_at: str) -> list[dict]:
    holdings = state.get("holdings", [])
    gains = 0
    losses = 0
    total_upnl = Decimal("0")
    for h in holdings:
        upnl = to_decimal(h.get("unrealizedPnl", "0"))
        total_upnl += upnl
        if upnl > 0:
            gains += 1
        elif upnl < 0:
            losses += 1
    bias = "risk_on" if total_upnl > 0 else "risk_off" if total_upnl < 0 else "neutral"
    return [{
        "kind": "portfolio_unrealized_pnl",
        "value": str(total_upnl),
        "gainers": gains,
        "losers": losses,
        "bias": bias,
        "asOf": state.get("asOf", generated_at),
        "source": "state.json",
    }]


def build_execution_constraints(state: dict, rules: dict, generated_at: str) -> list[dict]:
    out: list[dict] = []
    default_cutoff = (((rules.get("platforms") or {}).get("Alipay") or {}).get("defaultOrderCutoff")
                      if isinstance(rules, dict) else None) or "15:00"
    manual_required = state.get("manualExecutionRequiredFor", [])
    pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
    active_pending = [
        t for t in pending
        if str((t or {}).get("status", "")).upper() not in {"SETTLED", "CANCELLED", "FAILED"}
        and not str((t or {}).get("resolvedAt", "")).strip()
    ]

    overnight_pending_codes: list[str] = []
    overnight_buy_codes: list[str] = []
    overnight_redeem_codes: list[str] = []
    oldest_pending_created_at = ""
    cash = to_decimal(state.get("cash", "0"))
    if active_pending:
        today = datetime.now().date()
        created_ats = []
        for t in active_pending:
            created_at = str((t or {}).get("createdAt", "")).strip()
            if not created_at:
                continue
            try:
                created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                continue
            code = str((t or {}).get("code", "")).strip()
            action_type = str((t or {}).get("actionType", "")).upper()
            created_ats.append((created_dt, created_at, code, action_type))
        if created_ats:
            created_ats.sort(key=lambda x: x[0])
            oldest_pending_created_at = created_ats[0][1]
            for dt, _raw, code, action_type in created_ats:
                if dt.date() < today and code:
                    overnight_pending_codes.append(code)
                    if action_type == "BUY":
                        overnight_buy_codes.append(code)
                    elif action_type in {"REDEEM", "SELL"}:
                        overnight_redeem_codes.append(code)

    out.append({
        "kind": "manual_execution_requirement",
        "value": manual_required,
        "source": "state.json",
        "verifiedAt": generated_at,
    })
    blocking = False
    blocking_reason = ""
    if active_pending:
        if overnight_buy_codes:
            blocking = True
            blocking_reason = "overnight_buy_pending"
        elif overnight_redeem_codes and cash <= Decimal("0"):
            blocking = True
            blocking_reason = "overnight_redeem_with_no_cash"

    out.append({
        "kind": "pending_transaction_guard",
        "activeCount": len(active_pending),
        "blocking": blocking,
        "blockingReason": blocking_reason,
        "codes": [str((t or {}).get("code", "")).strip() for t in active_pending],
        "oldestCreatedAt": oldest_pending_created_at,
        "overnightCount": len(overnight_pending_codes),
        "overnightCodes": sorted(set(overnight_pending_codes)),
        "overnightBuyCount": len(set(overnight_buy_codes)),
        "overnightBuyCodes": sorted(set(overnight_buy_codes)),
        "overnightRedeemCount": len(set(overnight_redeem_codes)),
        "overnightRedeemCodes": sorted(set(overnight_redeem_codes)),
        "liquidCash": str(cash),
        "source": "state.json",
        "verifiedAt": generated_at,
    })
    target_value = to_decimal(((state.get("challenge") or {}).get("targetValue", "2000")))
    portfolio_value = to_decimal(compute(state).get("portfolioValue", "0"))
    out.append({
        "kind": "target_value_guard",
        "targetValue": str(target_value),
        "portfolioValue": str(portfolio_value),
        "targetReached": portfolio_value >= target_value,
        "actionBias": "no_new_buy" if portfolio_value >= target_value else "normal",
        "source": "state.json",
        "verifiedAt": generated_at,
    })
    out.append({
        "kind": "order_cutoff",
        "value": f"{default_cutoff} Asia/Shanghai",
        "source": "instrument_rules.json",
        "verifiedAt": generated_at,
    })

    funds = (rules.get("funds") or {}) if isinstance(rules, dict) else {}
    for h in state.get("holdings", []):
        code = str(h.get("code", "")).strip()
        settle = h.get("settlementRule") or ""
        rule = funds.get(code, {}) if isinstance(funds, dict) else {}
        confirm_rule = rule.get("confirmRule", "")
        settle_rule = rule.get("settleRule", "")
        out.append({
            "kind": "fund_settlement_rule",
            "code": code,
            "stateSettlement": settle,
            "ruleConfirm": confirm_rule,
            "ruleSettle": settle_rule,
            "source": "state.json+instrument_rules.json",
            "verifiedAt": generated_at,
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Build challenge evidence artifact")
    ap.add_argument("--state", required=True, help="Path to state.json")
    ap.add_argument("--template", required=True, help="Path to evidence template json")
    ap.add_argument("--outdir", required=True, help="Output evidence directory")
    ap.add_argument("--rules", default="fund_challenge/instrument_rules.json", help="Path to instrument rules")
    ap.add_argument("--strategy", default="fund_challenge/universe/strategy_mode.json", help="Path to strategy mode json")
    ap.add_argument("--candidates", default="fund_challenge/universe/daily_candidates.json", help="Path to daily candidates json")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    args = ap.parse_args()

    state = load_json(Path(args.state))
    tpl = load_json(Path(args.template))
    rules = load_optional_json(Path(args.rules))
    strategy = load_optional_json(Path(args.strategy))
    candidates = load_optional_json(Path(args.candidates))

    math = compute(state)

    decision_id = args.decision_id or f"decision-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    generated_at = now_zh_iso()

    evidence = dict(tpl)
    evidence["decisionId"] = decision_id
    evidence["phase"] = args.phase
    evidence["generatedAt"] = generated_at
    evidence["stateDigest"] = {
        "portfolioValue": math["portfolioValue"],
        "totalUnrealizedPnl": math["totalUnrealizedPnl"],
        "distanceToTarget": math["distanceToTarget"],
    }
    evidence["fundIdentityChecks"] = build_identity_checks(state, rules, generated_at)
    evidence["marketSignals"] = build_market_signals(state, generated_at)
    evidence["executionConstraints"] = build_execution_constraints(state, rules, generated_at)
    evidence["gateScoring"] = compute_gate_scoring(state, strategy, candidates)
    evidence["candidateScoring"] = build_candidate_scoring(candidates.get("candidates", []) if candidates else [], generated_at)
    evidence["arithmeticChecksum"] = checksum_state_digest(evidence["stateDigest"])

    # sync computed risk switch into market signal for traceability
    if isinstance(evidence.get("marketSignals"), list) and evidence["marketSignals"]:
        evidence["marketSignals"][0]["bias"] = evidence["gateScoring"]["riskSwitchComputed"]

    missing = []
    for k in ["fundIdentityChecks", "marketSignals", "executionConstraints"]:
        if not evidence.get(k):
            missing.append(k)

    if not isinstance(evidence.get("gateScoring"), dict):
        missing.append("gateScoring")

    if args.phase == "EXECUTE_READY" and missing:
        evidence["status"] = "ABORTED_MISSING_EVIDENCE"
    else:
        evidence["status"] = "READY" if args.phase == "EXECUTE_READY" else "PENDING_EVIDENCE"

    outdir = Path(args.outdir)
    out_file = outdir / f"{decision_id}.json"
    latest_file = outdir / "latest.json"
    save_json(out_file, evidence)
    save_json(latest_file, evidence)

    print(json.dumps({
        "status": "ok",
        "decisionId": decision_id,
        "phase": args.phase,
        "artifact": str(out_file),
        "latest": str(latest_file),
        "evidenceStatus": evidence["status"],
        "gateConsensus": bool((evidence.get("gateScoring") or {}).get("entryConsensus", {}).get("consistent", False)),
        "missing": missing,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
