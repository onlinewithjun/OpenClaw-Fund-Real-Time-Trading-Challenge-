from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STATE_FILE = WORKSPACE / "fund_challenge" / "runtime" / "state_refresh_retry.json"
MAX_RETRIES = 6


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(s: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def try_refresh() -> tuple[bool, str]:
    code, out, err = run([sys.executable, "fund_challenge/scripts/state_refresh.py"])
    if code == 0:
        return True, out or "STATE_REFRESH_OK"
    msg = out or err or "state_refresh_failed"
    return False, msg


def status_line() -> str:
    code, out, err = run([sys.executable, "fund_challenge/scripts/status_brief.py"])
    if code != 0:
        return f"status_brief_failed: {err or out}"
    return out


def handle_attempt(state: dict, is_init: bool) -> str:
    ok, msg = try_refresh()
    if ok:
        state.update({"active": False, "completed": True, "success": True, "lastError": ""})
        save_state(state)
        return f"UPDATE_OK | {status_line()}"

    # failed
    if not is_init:
        state["retries"] = int(state.get("retries", 0)) + 1

    retries = int(state.get("retries", 0))
    if retries >= int(state.get("maxRetries", MAX_RETRIES)):
        state.update({"active": False, "completed": True, "success": False, "lastError": msg})
        save_state(state)
        return f"UPDATE_ALERT retry_exhausted retries={retries}/{state.get('maxRetries', MAX_RETRIES)} reason={msg}"

    state.update({"active": True, "completed": False, "success": False, "lastError": msg})
    save_state(state)
    return f"UPDATE_RETRY_PENDING retries={retries}/{state.get('maxRetries', MAX_RETRIES)} reason={msg}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["init", "retry"], required=True)
    args = ap.parse_args()

    d = today()
    s = load_state()

    if args.mode == "init":
        s = {
            "date": d,
            "active": True,
            "completed": False,
            "success": False,
            "retries": 0,
            "maxRetries": MAX_RETRIES,
            "lastError": "",
            "updatedAt": datetime.now().isoformat(timespec="seconds"),
        }
        save_state(s)
        print(handle_attempt(s, is_init=True))
        return

    # retry mode
    if s.get("date") != d or not s.get("active", False):
        print("UPDATE_RETRY_SKIP no_active_retry")
        return

    print(handle_attempt(s, is_init=False))


if __name__ == "__main__":
    main()
