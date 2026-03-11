#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
UNIVERSE_DIR = WORKSPACE / "fund_challenge" / "universe"
MD_PATH = UNIVERSE_DIR / "daily_candidates.md"
JSON_PATH = UNIVERSE_DIR / "daily_candidates.json"


def fail(msg: str) -> None:
    print(f"UNIVERSE_REFRESH_ALERT: {msg}")
    raise SystemExit(1)


def now_cn_iso() -> str:
    # Keep explicit +08:00 for downstream freshness gates
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def parse_count(text: str, label: str) -> int:
    m = re.search(rf"\*\*{re.escape(label)}\*\*:\s*(\d+)", text)
    return int(m.group(1)) if m else 0


def parse_candidates(text: str) -> list[dict]:
    rows = []
    in_full_table = False
    for line in text.splitlines():
        if "## Full Candidate List" in line:
            in_full_table = True
            continue
        if in_full_table and line.startswith("## "):
            break
        if not in_full_table:
            continue
        if not line.strip().startswith("|"):
            continue

        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 7:
            continue
        if cols[0].lower() in {"code", "------"}:
            continue

        code, name, category, stage, confidence, source_url, verified_at = cols[:7]
        rows.append(
            {
                "code": code,
                "name": name,
                "category": category,
                "rationale": "derived from daily_candidates.md",
                "sourceUrl": source_url,
                "verifiedAt": verified_at,
                "confidence": confidence,
                "purchasableOn": ["tiantianfund", "alipay"],
                "stage": stage,
            }
        )
    return rows


def parse_bullets(text: str, header: str) -> list[str]:
    out: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.strip().startswith("### ") and header in line:
            in_section = True
            continue
        if in_section and line.strip().startswith("### "):
            break
        if in_section and line.strip().startswith("- "):
            out.append(line.strip()[2:])
    return out


def ensure_markdown_fresh_today(text: str) -> None:
    today = datetime.now().date().isoformat()
    m = re.search(r"#\s*Daily Fund Universe Refresh\s*-\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        fail("daily_candidates.md missing date header")
    header_date = m.group(1)
    if header_date != today:
        fail(f"stale markdown date: {header_date} != {today}")


def ensure_today_mtime(path: Path) -> None:
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    today = datetime.now().date()
    if mtime.date() != today:
        fail(f"json mtime not today: {mtime.isoformat()}")


def main() -> None:
    if not MD_PATH.exists():
        fail("daily_candidates.md missing")

    text = MD_PATH.read_text(encoding="utf-8", errors="replace")
    ensure_markdown_fresh_today(text)

    scanned_count = parse_count(text, "Scanned Count")
    refined_count = parse_count(text, "Deep Refined Count")
    candidates = parse_candidates(text)

    if not candidates:
        fail("no candidates parsed from markdown")

    payload = {
        "updatedAt": now_cn_iso(),
        "scanned_count": scanned_count,
        "refined_count": refined_count or len(candidates),
        "added": parse_bullets(text, "Added"),
        "removed": parse_bullets(text, "Removed"),
        "retained": parse_bullets(text, "Retained"),
        "candidates": candidates,
    }

    # write JSON first
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # read-back & mtime validation
    read_back = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if "updatedAt" not in read_back or not read_back.get("candidates"):
        fail("json read-back validation failed")
    ensure_today_mtime(JSON_PATH)

    print(
        f"UNIVERSE_REFRESH_OK json_updatedAt={read_back['updatedAt']} "
        f"json_mtime={datetime.fromtimestamp(JSON_PATH.stat().st_mtime).isoformat()} "
        f"scanned={payload['scanned_count']} refined={payload['refined_count']}"
    )


if __name__ == "__main__":
    main()
