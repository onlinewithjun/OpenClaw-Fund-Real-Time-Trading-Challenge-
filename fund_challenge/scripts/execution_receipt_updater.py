from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from state_math import compute


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def apply_receipt(state: dict, receipt: dict) -> dict:
    if not receipt.get("confirmed", False):
        raise ValueError("receipt.confirmed must be true")

    action_id = receipt.get("actionId")
    if not action_id:
        raise ValueError("receipt.actionId is required")

    out = deepcopy(state)

    # Optional cash overwrite
    if "cash" in receipt and receipt["cash"] is not None:
        out["cash"] = str(receipt["cash"])

    # Optional holdings patch list
    patches = receipt.get("holdingsPatch", [])
    if patches:
        code_to_h = {h.get("code"): h for h in out.get("holdings", [])}
        for p in patches:
            code = p.get("code")
            if not code or code not in code_to_h:
                raise ValueError(f"invalid holdings patch code: {code}")
            h = code_to_h[code]
            if "marketValue" in p and p["marketValue"] is not None:
                h["marketValue"] = str(p["marketValue"])
            if "unrealizedPnl" in p and p["unrealizedPnl"] is not None:
                h["unrealizedPnl"] = str(p["unrealizedPnl"])
            if "name" in p and p["name"]:
                h["name"] = p["name"]

    out["asOf"] = receipt.get("executedAt") or now_iso()
    out["lastUserConfirmedActionId"] = action_id

    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply confirmed execution receipt to challenge state + ledger")
    ap.add_argument("--state", required=True, help="Path to state.json")
    ap.add_argument("--ledger", required=True, help="Path to ledger.jsonl")
    ap.add_argument("--receipt", required=True, help="Path to execution receipt json")
    args = ap.parse_args()

    state_path = Path(args.state)
    ledger_path = Path(args.ledger)
    receipt_path = Path(args.receipt)

    state_before = load_json(state_path)
    receipt = load_json(receipt_path)

    state_after = apply_receipt(state_before, receipt)

    before_digest = compute(state_before)
    after_digest = compute(state_after)

    save_json(state_path, state_after)

    event = {
        "ts": now_iso(),
        "event": "execution_confirmed",
        "actionId": receipt.get("actionId"),
        "actionType": receipt.get("actionType"),
        "decisionId": receipt.get("decisionId"),
        "executedAt": receipt.get("executedAt"),
        "note": receipt.get("note", ""),
        "before": before_digest,
        "after": after_digest,
    }

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(json.dumps({
        "status": "ok",
        "actionId": receipt.get("actionId"),
        "state": str(state_path),
        "ledger": str(ledger_path),
        "before": before_digest,
        "after": after_digest,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
