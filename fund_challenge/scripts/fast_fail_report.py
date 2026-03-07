from __future__ import annotations

import argparse
import json
from pathlib import Path


FAIL_MAP = {
    "state_math": "STATE_MATH_FAILED",
    "refresh_instrument_rules": "RULE_REFRESH_FAILED",
    "build_evidence": "EVIDENCE_BUILD_FAILED",
    "validate_evidence": "EVIDENCE_VALIDATE_FAILED",
    "decision_publish_gate": "PUBLISH_GATE_FAILED",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate ultra-short fail report")
    ap.add_argument("--in", dest="inp", required=True, help="Input failure json")
    ap.add_argument("--out", required=True, help="Output txt")
    args = ap.parse_args()

    data = load_json(Path(args.inp))
    failed = data.get("failedAt", "unknown")
    code = FAIL_MAP.get(failed, "UNKNOWN_FAILURE")
    phase = data.get("phase", "N/A")

    msg = f"[ALERT] {code} | phase={phase} | step={failed} | action=HOLD"

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(msg + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(outp), "msg": msg}, ensure_ascii=False))


if __name__ == "__main__":
    main()
