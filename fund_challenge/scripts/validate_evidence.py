from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_TOP = [
    "decisionId",
    "phase",
    "generatedAt",
    "stateDigest",
    "fundIdentityChecks",
    "marketSignals",
    "executionConstraints",
    "arithmeticChecksum",
    "status",
]

REQUIRED_STATE_DIGEST = ["portfolioValue", "totalUnrealizedPnl", "distanceToTarget"]



def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))



def main() -> None:
    ap = argparse.ArgumentParser(description="Validate evidence artifact before EXECUTE_READY")
    ap.add_argument("--evidence", required=True, help="Path to evidence json")
    ap.add_argument("--require-execute-ready", action="store_true", help="Require phase=EXECUTE_READY and status=READY")
    args = ap.parse_args()

    p = Path(args.evidence)
    e = load_json(p)

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

    if args.require_execute_ready:
        if e.get("phase") != "EXECUTE_READY":
            errors.append("phase_not_execute_ready")
        if e.get("status") != "READY":
            errors.append("status_not_ready")

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
