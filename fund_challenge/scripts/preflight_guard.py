from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def shrink(text: str, max_chars: int = 220) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    return text if len(text) <= max_chars else text[: max_chars - 3] + "..."


def push_step(steps: list[dict], name: str, code: int, out: str, err: str, compact: bool) -> None:
    if compact:
        steps.append({
            "step": name,
            "ok": code == 0,
            "stdout": shrink(out),
            "stderr": shrink(err),
        })
    else:
        steps.append({"step": name, "ok": code == 0, "stdout": out, "stderr": err})


def main() -> None:
    ap = argparse.ArgumentParser(description="Challenge preflight guard pipeline")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--compact", action="store_true", help="Emit compact JSON to reduce token/output footprint")
    ap.add_argument("--with-publish-gate", action="store_true", help="Run strict decision_publish_gate in EXECUTE_READY")
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
    push_step(steps, "state_math", code, out, err, args.compact)
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
    push_step(steps, "refresh_instrument_rules", code, out, err, args.compact)
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
    push_step(steps, "build_evidence", code, out, err, args.compact)
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
    push_step(steps, "validate_evidence", code, out, err, args.compact)

    if args.phase == "EXECUTE_READY" and code != 0:
        print(json.dumps({"ok": False, "failedAt": "validate_evidence", "steps": steps}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    if args.with_publish_gate and args.phase == "EXECUTE_READY":
        c5 = [
            sys.executable,
            "fund_challenge/scripts/decision_publish_gate.py",
            "--evidence",
            "fund_challenge/evidence/latest.json",
            "--strict",
        ]
        code, out, err = run(c5, ws)
        push_step(steps, "decision_publish_gate", code, out, err, args.compact)
        if code != 0:
            print(json.dumps({"ok": False, "failedAt": "decision_publish_gate", "steps": steps}, ensure_ascii=False, indent=2))
            raise SystemExit(2)

    print(json.dumps({"ok": True, "phase": args.phase, "steps": steps}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
