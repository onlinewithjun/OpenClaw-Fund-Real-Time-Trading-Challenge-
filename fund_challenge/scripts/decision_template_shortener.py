from __future__ import annotations

import argparse
import json
from pathlib import Path


def short_line(d: dict) -> str:
    action = d.get("action", "HOLD")
    code = d.get("code", "N/A")
    name = d.get("name", "")
    amount = d.get("amountCny", "0")
    reason = d.get("reason", "No reason")
    deadline = d.get("deadline", "15:00 Asia/Shanghai")
    fallback = d.get("fallback", "HOLD")

    # concise telegram-safe single line
    return f"[{action}] {code} {name} {amount}CNY | {reason} | before {deadline} | fallback {fallback}".strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Shorten decision payload into low-token publish line")
    ap.add_argument("--in", dest="inp", required=True, help="Input json with decision fields")
    ap.add_argument("--out", required=True, help="Output txt path")
    ap.add_argument("--max-chars", type=int, default=220)
    args = ap.parse_args()

    data = json.loads(Path(args.inp).read_text(encoding="utf-8-sig"))
    line = short_line(data)
    if len(line) > args.max_chars:
        line = line[: args.max_chars - 3] + "..."

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(line + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "out": str(outp), "chars": len(line)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
