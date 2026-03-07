from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Link receipt decisionId from latest evidence")
    ap.add_argument("--receipt", required=True, help="Path to receipt json")
    ap.add_argument("--evidence", default="fund_challenge/evidence/latest.json", help="Path to latest evidence json")
    ap.add_argument("--force", action="store_true", help="Overwrite existing non-empty decisionId")
    args = ap.parse_args()

    rpath = Path(args.receipt)
    epath = Path(args.evidence)

    receipt = load_json(rpath)
    evidence = load_json(epath)

    old = str(receipt.get("decisionId") or "").strip()
    new = str(evidence.get("decisionId") or "").strip()
    if not new:
        raise SystemExit("evidence.decisionId is empty")

    if old and old != "" and not args.force:
        print(json.dumps({"status": "skip", "reason": "receipt already has decisionId", "decisionId": old}, ensure_ascii=False, indent=2))
        return

    receipt["decisionId"] = new
    save_json(rpath, receipt)

    print(json.dumps({"status": "ok", "receipt": str(rpath), "decisionId": new}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
