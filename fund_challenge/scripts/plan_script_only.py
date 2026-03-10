#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        return {}


def fail(msg: str) -> None:
    print(f"DECISION_ABORTED_UNVERIFIED_DATA HOLD # {msg}")
    raise SystemExit(1)


def main() -> None:
    code, out, err = run([
        sys.executable,
        "fund_challenge/scripts/preflight_guard.py",
        "--phase",
        "PLAN_ONLY",
        "--workspace",
        ".",
    ])
    if code != 0:
        fail(f"preflight_failed {err[:120]}")

    preflight = parse_json(out)
    if not preflight.get("ok"):
        fail("preflight_not_ok")

    validate = None
    for step in preflight.get("steps", []):
        if step.get("step") == "validate_evidence":
            validate = parse_json(step.get("stdout", ""))
            break

    if not validate:
        fail("validate_missing")

    if validate.get("ok") is not True:
        fail("validate_failed")

    status = str(validate.get("status", "UNKNOWN"))

    code2, out2, err2 = run([sys.executable, "fund_challenge/scripts/status_brief.py"])
    if code2 != 0:
        fail(f"status_brief_failed {err2[:120]}")

    if status != "READY":
        print(f"PLAN_ONLY HOLD | status={status} | {out2}")
        return

    # If status is READY, still keep conservative output under PLAN_ONLY.
    print(f"PLAN_ONLY READY_CHECK_PASS | {out2}")


if __name__ == "__main__":
    main()
