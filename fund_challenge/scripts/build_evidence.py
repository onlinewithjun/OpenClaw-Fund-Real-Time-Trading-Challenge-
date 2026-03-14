from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from gate_scoring import compute_gate_scoring
from state_math import compute


def now_zh_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


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


def build_identity_checks(state: dict, rules: dict, generated_at: str) -> list[dict]:
    funds = (rules.get("funds") or {}) if isinstance(rules, dict) else {}
    checks: list[dict] = []
    for h in state.get("holdings", []):
        code = str(h.get("code", "")).strip()
        name = str(h.get("name", "")).strip()
        rule = funds.get(code, {}) if isinstance(funds, dict) else {}
        rule_name = str(rule.get("name", "")).strip()
        matched = bool(code and name and rule_name and name == rule_name)
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
        if str((t or {}).get("status", "")).upper() not in {"SETTLED", "CANCELLED"}
    ]
    out.append({
        "kind": "manual_execution_requirement",
        "value": manual_required,
        "source": "state.json",
        "verifiedAt": generated_at,
    })
    out.append({
        "kind": "pending_transaction_guard",
        "activeCount": len(active_pending),
        "blocking": len(active_pending) > 0,
        "codes": [str((t or {}).get("code", "")).strip() for t in active_pending],
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
