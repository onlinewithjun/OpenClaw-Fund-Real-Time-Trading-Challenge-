from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def jloads_safe(s: str) -> dict:
    try:
        return json.loads(s)
    except Exception:
        return {"raw": s}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="End-to-end low-token decision pipeline")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--phase", default="PLAN_ONLY", choices=["PLAN_ONLY", "EXECUTE_READY"])
    ap.add_argument("--decision-id", default="")
    ap.add_argument("--action", default="HOLD")
    ap.add_argument("--code", default="N/A")
    ap.add_argument("--name", default="")
    ap.add_argument("--amount-cny", default="0")
    ap.add_argument("--reason", default="No verified reason")
    ap.add_argument("--deadline", default="15:00 Asia/Shanghai")
    ap.add_argument("--fallback", default="HOLD")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    did = args.decision_id or f"decision-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # 1 preflight
    c1 = [
        sys.executable,
        "fund_challenge/scripts/preflight_guard.py",
        "--phase", args.phase,
        "--decision-id", did,
        "--compact",
    ]
    if args.phase == "EXECUTE_READY":
        c1.append("--with-publish-gate")
    code1, out1, err1 = run(c1, ws)

    out_dir = ws / "fund_challenge" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    if code1 != 0:
        fail_json = out_dir / "preflight.fail.json"
        fail_json.write_text((out1 or "{}") + "\n", encoding="utf-8")
        cff = [
            sys.executable,
            "fund_challenge/scripts/fast_fail_report.py",
            "--in", str(fail_json),
            "--out", str(out_dir / "fail.short.txt"),
        ]
        codeff, outff, errff = run(cff, ws)
        print(json.dumps({
            "ok": False,
            "failedAt": "preflight_guard",
            "preflight": jloads_safe(out1),
            "fastFail": jloads_safe(outff) if codeff == 0 else {"raw": outff, "stderr": errff},
            "stderr": err1,
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 2 status brief
    c2 = [sys.executable, "fund_challenge/scripts/status_brief.py"]
    code2, out2, err2 = run(c2, ws)
    if code2 != 0:
        print(json.dumps({"ok": False, "failedAt": "status_brief", "stderr": err2}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    write_text(out_dir / "status.brief.txt", out2)

    # 3 compact evidence
    c3 = [
        sys.executable,
        "fund_challenge/scripts/evidence_compactor.py",
        "--in", "fund_challenge/evidence/latest.json",
        "--out", "fund_challenge/evidence/latest.compact.json",
    ]
    code3, out3, err3 = run(c3, ws)
    if code3 != 0:
        print(json.dumps({"ok": False, "failedAt": "evidence_compactor", "stderr": err3}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 4 decision short line
    decision_obj = {
        "action": args.action,
        "code": args.code,
        "name": args.name,
        "amountCny": args.amount_cny,
        "reason": args.reason,
        "deadline": args.deadline,
        "fallback": args.fallback,
    }
    dpath = out_dir / "decision.json"
    dpath.write_text(json.dumps(decision_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    c4 = [
        sys.executable,
        "fund_challenge/scripts/decision_template_shortener.py",
        "--in", str(dpath),
        "--out", "fund_challenge/out/decision.short.txt",
    ]
    code4, out4, err4 = run(c4, ws)
    if code4 != 0:
        print(json.dumps({"ok": False, "failedAt": "decision_template_shortener", "stderr": err4}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    # 5 packet
    c5 = [
        sys.executable,
        "fund_challenge/scripts/decision_packet_builder.py",
        "--decision-id", did,
        "--phase", args.phase,
        "--evidence", "fund_challenge/evidence/latest.compact.json",
        "--short-line", "fund_challenge/out/decision.short.txt",
        "--status-brief", "fund_challenge/out/status.brief.txt",
        "--out", "fund_challenge/out/decision.packet.json",
    ]
    code5, out5, err5 = run(c5, ws)
    if code5 != 0:
        print(json.dumps({"ok": False, "failedAt": "decision_packet_builder", "stderr": err5}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    print(json.dumps({
        "ok": True,
        "decisionId": did,
        "phase": args.phase,
        "preflight": jloads_safe(out1),
        "statusBrief": out2,
        "packet": jloads_safe(out5),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
