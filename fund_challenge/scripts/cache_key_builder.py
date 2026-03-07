from __future__ import annotations

import argparse
import hashlib
import json


def main() -> None:
    ap = argparse.ArgumentParser(description="Build stable cache key for source fetch")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--code", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--date", required=True)
    args = ap.parse_args()

    base = f"{args.provider}|{args.code}|{args.topic}|{args.date}"
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:20]
    print(json.dumps({"ok": True, "key": f"src:{digest}", "base": base}, ensure_ascii=False))


if __name__ == "__main__":
    main()
