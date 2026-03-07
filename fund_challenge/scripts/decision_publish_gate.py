from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Gate publisher for challenge trade instructions")
    ap.add_argument("--evidence", required=True, help="Path to evidence json")
    ap.add_argument("--strict", action="store_true", help="Require EXECUTE_READY and READY status")
    args = ap.parse_args()

    e = load_json(Path(args.evidence))
    phase = e.get("phase")
    status = e.get("status")

    reasons: list[str] = []

    if args.strict:
        if phase != "EXECUTE_READY":
            reasons.append("phase_not_execute_ready")
        if status != "READY":
            reasons.append("status_not_ready")

    for key in ["fundIdentityChecks", "marketSignals", "executionConstraints"]:
        if not isinstance(e.get(key), list) or len(e.get(key)) == 0:
            reasons.append(f"missing_or_empty_{key}")

    allowed = len(reasons) == 0

    if allowed:
        result = {
            "allowed": True,
            "publishMode": "EXECUTABLE_INSTRUCTION",
            "decisionId": e.get("decisionId"),
            "phase": phase,
            "status": status,
        }
    else:
        result = {
            "allowed": False,
            "publishMode": "HOLD_ONLY",
            "decisionId": e.get("decisionId"),
            "phase": phase,
            "status": status,
            "reasons": reasons,
            "requiredOutput": "DECISION_ABORTED_UNVERIFIED_DATA",
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not allowed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
