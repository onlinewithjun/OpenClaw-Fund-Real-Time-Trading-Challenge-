from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


REQUIRED_TOP = [
    "decisionId",
    "phase",
    "generatedAt",
    "stateDigest",
    "fundIdentityChecks",
    "marketSignals",
    "executionConstraints",
    "gateScoring",
    "decisionFramework",
    "arithmeticChecksum",
    "status",
]

REQUIRED_STATE_DIGEST = ["portfolioValue", "totalUnrealizedPnl", "distanceToTarget"]
REQUIRED_GATE_SCORING = ["riskSwitchComputed", "momentumGate", "drawdownGate", "oversoldRotationChannel", "entryConsensus"]
REQUIRED_FRAMEWORK_WEIGHTS = {"macro": 0.30, "sentiment": 0.25, "sector": 0.25, "quant": 0.20}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _date_part(ts: str) -> str:
    if not ts:
        return ""
    # supports both 2026-03-10T.. and 2026-03-10 .. formats
    return str(ts).split("T", 1)[0].split(" ", 1)[0]


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate evidence artifact before EXECUTE_READY")
    ap.add_argument("--evidence", required=True, help="Path to evidence json")
    ap.add_argument("--require-execute-ready", action="store_true", help="Require phase=EXECUTE_READY and status=READY")
    args = ap.parse_args()

    e = load_json(Path(args.evidence))
    errors: list[str] = []

    for k in REQUIRED_TOP:
        if k not in e:
            errors.append(f"missing_top_field:{k}")

    digest = e.get("stateDigest", {}) if isinstance(e.get("stateDigest"), dict) else {}
    for k in REQUIRED_STATE_DIGEST:
        if k not in digest or digest.get(k) in (None, ""):
            errors.append(f"missing_state_digest_field:{k}")

    for k in ["fundIdentityChecks", "marketSignals", "executionConstraints"]:
        v = e.get(k)
        if not isinstance(v, list) or len(v) == 0:
            errors.append(f"empty_array_field:{k}")

    gs = e.get("gateScoring") if isinstance(e.get("gateScoring"), dict) else {}
    if not gs:
        errors.append("missing_gate_scoring")
    else:
        for k in REQUIRED_GATE_SCORING:
            if k not in gs:
                errors.append(f"missing_gate_scoring_field:{k}")

    framework = e.get("decisionFramework") if isinstance(e.get("decisionFramework"), dict) else {}
    weights = framework.get("weights") if isinstance(framework.get("weights"), dict) else {}
    if not framework:
        errors.append("missing_decision_framework")
    else:
        for k, expected in REQUIRED_FRAMEWORK_WEIGHTS.items():
            actual = weights.get(k)
            if actual != expected:
                errors.append(f"decision_framework_weight_mismatch:{k}={actual}")
        if framework.get("quantRole") != "reference_only":
            errors.append(f"decision_framework_quant_role_invalid:{framework.get('quantRole')}")

    candidate_scoring = e.get("candidateScoring") if isinstance(e.get("candidateScoring"), dict) else {}
    alipay_filter = candidate_scoring.get("alipayFilter") if isinstance(candidate_scoring.get("alipayFilter"), dict) else {}
    if candidate_scoring and alipay_filter.get("blockedCount", 0):
        errors.append(f"candidate_not_alipay_allowed:{','.join(alipay_filter.get('blockedCodes', []))}")

    if args.require_execute_ready:
        if e.get("phase") != "EXECUTE_READY":
            errors.append("phase_not_execute_ready")
        if e.get("status") != "READY":
            errors.append("status_not_ready")

        asof = ""
        ms = e.get("marketSignals")
        if isinstance(ms, list) and ms:
            asof = str((ms[0] or {}).get("asOf", ""))
        today = datetime.now().strftime("%Y-%m-%d")
        if _date_part(asof) != today:
            errors.append(f"stale_state_asof:{asof}")

    result = {
        "ok": len(errors) == 0,
        "errors": errors,
        "decisionId": e.get("decisionId"),
        "phase": e.get("phase"),
        "status": e.get("status"),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
