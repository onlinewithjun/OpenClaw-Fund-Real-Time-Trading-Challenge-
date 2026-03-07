from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


ACTION_MAP = {
    "买入": "BUY",
    "申购": "BUY",
    "加仓": "BUY",
    "卖出": "REDEEM",
    "赎回": "REDEEM",
    "减仓": "REDEEM",
    "转换": "SWITCH",
    "调仓": "SWITCH",
    "持有": "HOLD",
}


def detect_action(text: str) -> str:
    for k, v in ACTION_MAP.items():
        if k in text:
            return v
    return "BUY"


def extract_code(text: str) -> str | None:
    m = re.search(r"\b(\d{6})\b", text)
    return m.group(1) if m else None


def extract_amount(text: str) -> str | None:
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*元", text)
    if m:
        return m.group(1)
    m = re.search(r"金额\s*[:：]\s*([0-9]+(?:\.[0-9]+)?)", text)
    return m.group(1) if m else None


def extract_name(text: str) -> str | None:
    # Best effort: text between code and amount, or after action keyword
    m = re.search(r"\b\d{6}\b\s*([\u4e00-\u9fa5A-Za-z0-9ETF联接发起主题指数\-\s]{2,40})", text)
    if m:
        name = m.group(1).strip()
        name = re.sub(r"([0-9]+(?:\.[0-9]+)?\s*元).*$", "", name).strip()
        return name or None
    return None


def parse_text(text: str) -> dict:
    action = detect_action(text)
    code = extract_code(text)
    amount = extract_amount(text)
    name = extract_name(text)

    now = datetime.now().replace(microsecond=0).isoformat()
    action_id = f"act-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    decision_id = f"decision-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    receipt = {
        "confirmed": True,
        "actionId": action_id,
        "decisionId": decision_id,
        "actionType": action,
        "executedAt": now,
        "cash": None,
        "holdingsPatch": [],
        "tradeAmountCny": amount,
        "note": "Parsed from user text confirmation",
        "rawText": text,
    }

    if code:
        patch = {"code": code}
        if name:
            patch["name"] = name
        # Safety default: do not map trade amount directly to marketValue.
        # marketValue/unrealizedPnl should be patched only with explicit portfolio snapshot data.
        receipt["holdingsPatch"].append(patch)

    return receipt


def main() -> None:
    ap = argparse.ArgumentParser(description="Parse execution confirmation text into receipt.json")
    ap.add_argument("--text", help="Inline confirmation text")
    ap.add_argument("--text-file", help="Path to text file containing confirmation")
    ap.add_argument("--out", required=True, help="Output receipt json path")
    args = ap.parse_args()

    if not args.text and not args.text_file:
        raise SystemExit("Provide --text or --text-file")

    if args.text:
        text = args.text.strip()
    else:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()

    receipt = parse_text(text)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": "ok", "out": str(out), "receipt": receipt}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
