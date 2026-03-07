from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def fp(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Prevent duplicate same-day decision publishing")
    ap.add_argument("--decision-text", required=True, help="Canonical decision text")
    ap.add_argument("--decision-id", default="")
    ap.add_argument("--history", default="fund_challenge/decision_history.jsonl")
    ap.add_argument("--record", action="store_true", help="Record fingerprint when not duplicate")
    args = ap.parse_args()

    history_path = Path(args.history)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    digest = fp(args.decision_text)
    day = today_key()

    dup = False
    if history_path.exists():
        for line in history_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            if row.get("day") == day and row.get("fingerprint") == digest:
                dup = True
                break

    if dup:
        print(json.dumps({"ok": False, "duplicate": True, "day": day, "decisionId": args.decision_id}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    if args.record:
        row = {
            "ts": datetime.now().replace(microsecond=0).isoformat(),
            "day": day,
            "decisionId": args.decision_id,
            "fingerprint": digest,
        }
        with history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(json.dumps({"ok": True, "duplicate": False, "day": day, "decisionId": args.decision_id, "recorded": bool(args.record)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
