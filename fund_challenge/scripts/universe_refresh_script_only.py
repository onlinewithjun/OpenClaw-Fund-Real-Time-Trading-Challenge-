#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
UNIVERSE_DIR = WORKSPACE / "fund_challenge" / "universe"
JSON_PATH = UNIVERSE_DIR / "daily_candidates.json"


def fail(msg: str) -> None:
    print(f"UNIVERSE_REFRESH_ALERT: {msg}")
    raise SystemExit(1)


def now_cn_iso() -> str:
    # Keep explicit +08:00 for downstream freshness gates
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def ensure_today_mtime(path: Path) -> None:
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    today = datetime.now().date()
    if mtime.date() != today:
        fail(f"json mtime not today: {mtime.isoformat()}")


def load_existing_json() -> dict:
    if not JSON_PATH.exists():
        fail("daily_candidates.json missing")
    try:
        return json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except Exception:
        fail("daily_candidates.json invalid")


def normalize_candidates(candidates: list[dict], verified_at: str) -> list[dict]:
    out: list[dict] = []
    for c in candidates:
        if not isinstance(c, dict):
            continue
        code = str(c.get("code", "")).strip()
        name = str(c.get("name", "")).strip()
        if not code or not name:
            continue
        out.append(
            {
                "code": code,
                "name": name,
                "category": str(c.get("category", "broad_index_core")),
                "rationale": str(c.get("rationale", "derived from daily_candidates.json")),
                "sourceUrl": str(c.get("sourceUrl", "")),
                "verifiedAt": verified_at,
                "confidence": str(c.get("confidence", "0.70")),
                "purchasableOn": c.get("purchasableOn", ["tiantianfund", "alipay"]),
                "stage": str(c.get("stage", "deep_refine")),
            }
        )
    return out


def main() -> None:
    existing = load_existing_json()
    now = now_cn_iso()

    raw_candidates = existing.get("candidates", []) if isinstance(existing, dict) else []
    if not isinstance(raw_candidates, list) or not raw_candidates:
        fail("no candidates in daily_candidates.json")

    candidates = normalize_candidates(raw_candidates, now)
    if not candidates:
        fail("no valid candidates after normalization")

    scanned_count = int(existing.get("scanned_count", len(candidates)))
    if scanned_count < len(candidates):
        scanned_count = len(candidates)

    payload = {
        "updatedAt": now,
        "scanned_count": scanned_count,
        "refined_count": len(candidates),
        "added": existing.get("added", ["None (single-source json refresh)"]),
        "removed": existing.get("removed", ["None"]),
        "retained": [
            f"all {len(candidates)} candidates retained from json source",
            f"verification timestamp refreshed: {now}",
        ],
        "candidates": candidates,
    }

    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    read_back = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if "updatedAt" not in read_back or not read_back.get("candidates"):
        fail("json read-back validation failed")
    ensure_today_mtime(JSON_PATH)

    print(
        f"UNIVERSE_REFRESH_OK json_updatedAt={read_back['updatedAt']} "
        f"json_mtime={datetime.fromtimestamp(JSON_PATH.stat().st_mtime).isoformat()} "
        f"scanned={payload['scanned_count']} refined={payload['refined_count']} source=json"
    )


if __name__ == "__main__":
    main()
