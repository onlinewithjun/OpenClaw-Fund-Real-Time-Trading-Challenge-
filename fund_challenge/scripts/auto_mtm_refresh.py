from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Auto mark-to-market refresh if nav snapshot exists")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--snapshot", default="fund_challenge/nav_snapshot.json")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--ledger", default="fund_challenge/ledger.jsonl")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    snapshot = ws / args.snapshot

    if not snapshot.exists():
        print("NAV_SNAPSHOT_MISSING | no mtm update")
        return

    c1 = [
        sys.executable,
        "fund_challenge/scripts/apply_mark_to_market.py",
        "--state",
        args.state,
        "--ledger",
        args.ledger,
        "--snapshot",
        args.snapshot,
    ]
    code1, out1, err1 = run(c1, ws)
    if code1 != 0:
        print(f"NAV_REFRESH_FAILED | {err1 or out1}")
        raise SystemExit(2)

    c2 = [sys.executable, "fund_challenge/scripts/status_brief.py"]
    code2, out2, err2 = run(c2, ws)
    if code2 != 0:
        print(f"NAV_REFRESH_OK | status_brief_failed | {err2}")
        return

    sys.stdout.buffer.write(out2.encode("gbk", errors="replace") + b"\n")


if __name__ == "__main__":
    main()
