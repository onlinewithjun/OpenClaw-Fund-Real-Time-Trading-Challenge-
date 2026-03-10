from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STATE_PATH = WORKSPACE / "fund_challenge" / "state.json"


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def date_part(ts: str) -> str:
    return str(ts).split("T", 1)[0].split(" ", 1)[0]


def main() -> None:
    code, out, err = run([
        sys.executable,
        "fund_challenge/scripts/auto_mtm_refresh.py",
        "--workspace",
        ".",
    ])
    if code != 0:
        print(f"STATE_REFRESH_ALERT: auto_mtm_failed | {err or out}")
        raise SystemExit(1)

    if not STATE_PATH.exists():
        print("STATE_REFRESH_ALERT: state.json_missing")
        raise SystemExit(1)

    state = load_json(STATE_PATH)
    asof = str(state.get("asOf", ""))
    today = datetime.now().strftime("%Y-%m-%d")
    if date_part(asof) != today:
        print(f"STATE_REFRESH_ALERT: stale_asof={asof}")
        raise SystemExit(1)

    print(f"STATE_REFRESH_OK asOf={asof}")


if __name__ == "__main__":
    main()
