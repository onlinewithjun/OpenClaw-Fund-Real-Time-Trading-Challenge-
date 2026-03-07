from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def jloads_safe(s: str) -> dict:
    try:
        return json.loads(s)
    except Exception:
        return {"raw": s}


def main() -> None:
    ap = argparse.ArgumentParser(description="Low-token daily challenge runner")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--with-publish-gate", action="store_true")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()

    c1 = [
        sys.executable,
        "fund_challenge/scripts/preflight_guard.py",
        "--phase",
        args.phase,
        "--compact",
    ]
    if args.decision_id:
        c1.extend(["--decision-id", args.decision_id])
    if args.with_publish_gate:
        c1.append("--with-publish-gate")

    code1, out1, err1 = run(c1, ws)
    if code1 != 0:
        print(json.dumps({"ok": False, "failedAt": "preflight_guard", "detail": jloads_safe(out1), "stderr": err1}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    c2 = [sys.executable, "fund_challenge/scripts/status_brief.py"]
    code2, out2, err2 = run(c2, ws)
    if code2 != 0:
        print(json.dumps({"ok": False, "failedAt": "status_brief", "stderr": err2}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    print(json.dumps({
        "ok": True,
        "phase": args.phase,
        "statusBrief": out2,
        "preflight": jloads_safe(out1),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
