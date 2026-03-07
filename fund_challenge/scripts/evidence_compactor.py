from __future__ import annotations

import argparse
import json
from pathlib import Path


KEEP_TOP = {
    "decisionId",
    "phase",
    "generatedAt",
    "stateDigest",
    "fundIdentityChecks",
    "marketSignals",
    "executionConstraints",
    "arithmeticChecksum",
    "status",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compact_list(items: list, max_items: int) -> list:
    if not isinstance(items, list):
        return []
    out = []
    for it in items[:max_items]:
        if isinstance(it, dict):
            # Keep only high-signal keys when present
            keep = {}
            for k in ["code", "name", "ok", "source", "timestamp", "signal", "score", "constraint", "value"]:
                if k in it:
                    keep[k] = it[k]
            out.append(keep or it)
        else:
            out.append(it)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Compact evidence JSON for low-token runtime")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-identity", type=int, default=5)
    ap.add_argument("--max-signals", type=int, default=6)
    ap.add_argument("--max-constraints", type=int, default=6)
    args = ap.parse_args()

    src = load_json(Path(args.inp))
    out = {k: src.get(k) for k in KEEP_TOP if k in src}

    out["fundIdentityChecks"] = compact_list(src.get("fundIdentityChecks", []), args.max_identity)
    out["marketSignals"] = compact_list(src.get("marketSignals", []), args.max_signals)
    out["executionConstraints"] = compact_list(src.get("executionConstraints", []), args.max_constraints)

    raw_size = len(json.dumps(src, ensure_ascii=False))
    new_size = len(json.dumps(out, ensure_ascii=False))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "in": str(args.inp),
        "out": str(out_path),
        "rawSize": raw_size,
        "compactSize": new_size,
        "saved": max(0, raw_size - new_size),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
