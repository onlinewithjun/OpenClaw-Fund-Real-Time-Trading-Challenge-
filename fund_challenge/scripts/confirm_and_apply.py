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
    ap = argparse.ArgumentParser(description="One-shot: parse confirmation text then apply receipt update")
    ap.add_argument("--text", help="Confirmation text")
    ap.add_argument("--text-file", help="Path to text file")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--receipt-out", default="fund_challenge/receipt.json")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--ledger", default="fund_challenge/ledger.jsonl")
    ap.add_argument("--evidence", default="fund_challenge/evidence/latest.json")
    ap.add_argument("--link-decision-id", action="store_true", help="Link receipt decisionId from latest evidence")
    args = ap.parse_args()

    if not args.text and not args.text_file:
        raise SystemExit("Provide --text or --text-file")

    ws = Path(args.workspace).resolve()
    receipt_out = args.receipt_out

    c1 = [
        sys.executable,
        "fund_challenge/scripts/receipt_from_text.py",
        "--out",
        receipt_out,
    ]
    if args.text:
        c1.extend(["--text", args.text])
    else:
        c1.extend(["--text-file", args.text_file])

    code1, out1, err1 = run(c1, ws)
    if code1 != 0:
        print(json.dumps({"ok": False, "failedAt": "receipt_from_text", "stdout": out1, "stderr": err1}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    link_out = ""
    if args.link_decision_id:
        c_link = [
            sys.executable,
            "fund_challenge/scripts/decision_id_linker.py",
            "--receipt",
            receipt_out,
            "--evidence",
            args.evidence,
            "--force",
        ]
        code_link, link_out, err_link = run(c_link, ws)
        if code_link != 0:
            print(json.dumps({"ok": False, "failedAt": "decision_id_linker", "stdout": link_out, "stderr": err_link}, ensure_ascii=False, indent=2))
            raise SystemExit(2)

    c2 = [
        sys.executable,
        "fund_challenge/scripts/execution_receipt_updater.py",
        "--state",
        args.state,
        "--ledger",
        args.ledger,
        "--receipt",
        receipt_out,
    ]
    code2, out2, err2 = run(c2, ws)
    if code2 != 0:
        print(json.dumps({"ok": False, "failedAt": "execution_receipt_updater", "stdout": out2, "stderr": err2}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    print(json.dumps({
        "ok": True,
        "receipt": receipt_out,
        "parse": out1,
        "link": link_out,
        "apply": out2,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
