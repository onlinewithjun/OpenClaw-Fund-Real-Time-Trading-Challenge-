from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


CACHE_PATH = Path("fund_challenge/cache/runtime_cache.json")


def load_cache(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {"items": {}}
    return {"items": {}}


def save_cache(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def k(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]


def cmd_get(args: argparse.Namespace) -> int:
    c = load_cache(Path(args.cache))
    key = k(args.key)
    item = c.get("items", {}).get(key)
    if not item:
        print(json.dumps({"hit": False}, ensure_ascii=False))
        return 1
    now = int(time.time())
    if item.get("expireAt") and now > int(item["expireAt"]):
        print(json.dumps({"hit": False, "expired": True}, ensure_ascii=False))
        return 1
    print(json.dumps({"hit": True, "value": item.get("value"), "meta": item.get("meta", {})}, ensure_ascii=False))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    c = load_cache(Path(args.cache))
    key = k(args.key)
    ttl = max(0, int(args.ttl_sec))
    now = int(time.time())
    exp = now + ttl if ttl > 0 else None

    value = args.value
    if args.value_file:
        value = Path(args.value_file).read_text(encoding="utf-8")

    meta = {}
    if args.meta:
        try:
            meta = json.loads(args.meta)
        except Exception:
            meta = {"raw": args.meta}

    c.setdefault("items", {})[key] = {
        "originalKey": args.key,
        "value": value,
        "meta": meta,
        "updatedAt": now,
        "expireAt": exp,
    }
    save_cache(Path(args.cache), c)
    print(json.dumps({"ok": True, "key": key, "expireAt": exp}, ensure_ascii=False))
    return 0


def cmd_prune(args: argparse.Namespace) -> int:
    path = Path(args.cache)
    c = load_cache(path)
    now = int(time.time())
    items = c.get("items", {})
    kept = {}
    removed = 0
    for kk, vv in items.items():
        exp = vv.get("expireAt")
        if exp and now > int(exp):
            removed += 1
            continue
        kept[kk] = vv
    c["items"] = kept
    save_cache(path, c)
    print(json.dumps({"ok": True, "removed": removed, "remain": len(kept)}, ensure_ascii=False))
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Tiny runtime cache for low-token challenge operations")
    ap.add_argument("--cache", default=str(CACHE_PATH))
    sp = ap.add_subparsers(dest="cmd", required=True)

    g = sp.add_parser("get")
    g.add_argument("--key", required=True)
    g.set_defaults(func=cmd_get)

    s = sp.add_parser("set")
    s.add_argument("--key", required=True)
    s.add_argument("--value", default="")
    s.add_argument("--value-file")
    s.add_argument("--ttl-sec", default="900")
    s.add_argument("--meta", default="{}")
    s.set_defaults(func=cmd_set)

    p = sp.add_parser("prune")
    p.set_defaults(func=cmd_prune)

    args = ap.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
