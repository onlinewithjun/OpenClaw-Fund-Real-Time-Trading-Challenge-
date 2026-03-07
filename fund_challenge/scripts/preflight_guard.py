from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Challenge preflight guard pipeline")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    ap.add_argument("--workspace", default=".")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()

    steps: list[dict] = []

    # 1) deterministic math
    c1 = [
        sys.executable,
        "fund_challenge/scripts/state_math.py",
        "--state",
        "fund_challenge/state.json",
    ]
    code, out, err = run(c1, ws)
    steps.append({"step": "state_math", "ok": code == 0, "stdout": out, "stderr": err})
    if code != 0:
        print(json.dumps({"ok": False, "failedAt": "state_math", "steps": steps}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 2) refresh instrument rules metadata
    c2 = [
        sys.executable,
        "fund_challenge/scripts/refresh_instrument_rules.py",
        "--rules",
        "fund_challenge/instrument_rules.json",
        "--sources",
        "fund_challenge/instrument_rule_sources.json",
    ]
    code, out, err = run(c2, ws)
    steps.append({"step": "refresh_instrument_rules", "ok": code == 0, "stdout": out, "stderr": err})
    if code != 0:
        print(json.dumps({"ok": False, "failedAt": "refresh_instrument_rules", "steps": steps}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 3) build evidence
    c3 = [
        sys.executable,
        "fund_challenge/scripts/build_evidence.py",
        "--state",
        "fund_challenge/state.json",
        "--template",
        "fund_challenge/evidence/template.json",
        "--outdir",
        "fund_challenge/evidence",
        "--phase",
        args.phase,
    ]
    if args.decision_id:
        c3.extend(["--decision-id", args.decision_id])

    code, out, err = run(c3, ws)
    steps.append({"step": "build_evidence", "ok": code == 0, "stdout": out, "stderr": err})
    if code != 0:
        print(json.dumps({"ok": False, "failedAt": "build_evidence", "steps": steps}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 4) validate evidence hard gate
    c4 = [
        sys.executable,
        "fund_challenge/scripts/validate_evidence.py",
        "--evidence",
        "fund_challenge/evidence/latest.json",
    ]
    if args.phase == "EXECUTE_READY":
        c4.append("--require-execute-ready")

    code, out, err = run(c4, ws)
    steps.append({"step": "validate_evidence", "ok": code == 0, "stdout": out, "stderr": err})

    if args.phase == "EXECUTE_READY" and code != 0:
        print(json.dumps({"ok": False, "failedAt": "validate_evidence", "steps": steps}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    print(json.dumps({"ok": True, "phase": args.phase, "steps": steps}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
