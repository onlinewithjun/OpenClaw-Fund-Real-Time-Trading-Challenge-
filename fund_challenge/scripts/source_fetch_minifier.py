from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[。！？!?\.])\s+|\n+", text)
    return [c.strip() for c in chunks if c.strip()]


def score_line(line: str, keywords: list[str]) -> int:
    s = 0
    low = line.lower()
    for kw in keywords:
        if kw.lower() in low:
            s += 3
    if re.search(r"\d", line):
        s += 1
    if any(x in line for x in ["截止", "T+", "%", "公告", "确认", "赎回", "申购"]):
        s += 2
    return s


def minify(text: str, keywords: list[str], max_lines: int, max_chars: int) -> dict:
    sents = split_sentences(text)
    ranked = sorted(((score_line(x, keywords), i, x) for i, x in enumerate(sents)), key=lambda t: (-t[0], t[1]))
    picked = [x for sc, _, x in ranked if sc > 0][:max_lines]
    if not picked:
        picked = sents[:max_lines]
    joined = "\n".join(picked)
    if len(joined) > max_chars:
        joined = joined[: max_chars - 3] + "..."
    return {"summary": joined, "picked": len(picked), "total": len(sents)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Minify fetched source text for low-token evidence usage")
    ap.add_argument("--in", dest="inp", required=True, help="Input text/json file path")
    ap.add_argument("--out", required=True, help="Output json path")
    ap.add_argument("--keywords", default="基金,申购,赎回,T+,截止,公告,确认")
    ap.add_argument("--max-lines", type=int, default=8)
    ap.add_argument("--max-chars", type=int, default=1200)
    args = ap.parse_args()

    p = Path(args.inp)
    raw = p.read_text(encoding="utf-8")

    # If input is JSON, try common fields
    text = raw
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            text = str(obj.get("text") or obj.get("content") or obj.get("markdown") or raw)
    except Exception:
        pass

    kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
    out = minify(text, kws, args.max_lines, args.max_chars)
    out["keywords"] = kws

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(outp), "picked": out["picked"], "total": out["total"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
