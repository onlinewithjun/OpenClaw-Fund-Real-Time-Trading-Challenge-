from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

from state_math import compute  # same directory import


def now_zh_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def checksum_state_digest(digest: dict) -> str:
    payload = json.dumps(digest, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description="Build challenge evidence artifact")
    ap.add_argument("--state", required=True, help="Path to state.json")
    ap.add_argument("--template", required=True, help="Path to evidence template json")
    ap.add_argument("--outdir", required=True, help="Output evidence directory")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    args = ap.parse_args()

    state = load_json(Path(args.state))
    tpl = load_json(Path(args.template))
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
    evidence["arithmeticChecksum"] = checksum_state_digest(evidence["stateDigest"])

    missing = []
    for k in ["fundIdentityChecks", "marketSignals", "executionConstraints"]:
        if not evidence.get(k):
            missing.append(k)

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
        "missing": missing,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
