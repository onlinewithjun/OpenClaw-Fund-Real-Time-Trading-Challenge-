from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Build compact decision packet for publishing")
    ap.add_argument("--decision-id", required=True)
    ap.add_argument("--phase", default="EXECUTE_READY")
    ap.add_argument("--evidence", default="fund_challenge/evidence/latest.compact.json")
    ap.add_argument("--short-line", default="fund_challenge/out/decision.short.txt")
    ap.add_argument("--status-brief", default="fund_challenge/out/status.brief.txt")
    ap.add_argument("--out", default="fund_challenge/out/decision.packet.json")
    args = ap.parse_args()

    evidence = load_json(Path(args.evidence))
    short_line = load_text(Path(args.short_line))
    status_brief = load_text(Path(args.status_brief)) if Path(args.status_brief).exists() else ""

    packet = {
        "decisionId": args.decision_id,
        "phase": args.phase,
        "status": evidence.get("status", "UNKNOWN"),
        "stateDigest": evidence.get("stateDigest", {}),
        "line": short_line,
        "statusBrief": status_brief,
        "evidenceRef": str(Path(args.evidence)),
        "checks": {
            "identityCount": len(evidence.get("fundIdentityChecks", [])),
            "signalCount": len(evidence.get("marketSignals", [])),
            "constraintCount": len(evidence.get("executionConstraints", [])),
        },
    }

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(outp), "decisionId": args.decision_id}, ensure_ascii=False))


if __name__ == "__main__":
    main()
