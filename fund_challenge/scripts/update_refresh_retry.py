from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STATE_FILE = WORKSPACE / "fund_challenge" / "runtime" / "state_refresh_retry.json"
STATE_JSON = WORKSPACE / "fund_challenge" / "state.json"
SNAPSHOT_JSON = WORKSPACE / "fund_challenge" / "nav_snapshot.json"
RECEIPT_JSON = WORKSPACE / "fund_challenge" / "receipt.json"
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


def d(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def q2(v: Decimal) -> str:
    return str(v.quantize(Decimal("0.01")))


def status_line() -> str:
    code, out, err = run([sys.executable, "fund_challenge/scripts/status_brief.py"])
    if code != 0:
        return f"status_brief_failed: {err or out}"
    return out


def parse_status_metrics(line: str) -> dict:
    out = {"PV": "-", "UPnL": "-", "Gap": "-"}
    for part in line.split("|"):
        p = part.strip()
        if p.startswith("PV "):
            out["PV"] = p.replace("PV ", "").strip()
        elif p.startswith("UPnL "):
            out["UPnL"] = p.replace("UPnL ", "").strip()
        elif p.startswith("Gap "):
            out["Gap"] = p.replace("Gap ", "").strip()
    return out


def load_snapshot_today_pnl_map() -> dict:
    if not SNAPSHOT_JSON.exists():
        return {}
    try:
        snap = json.loads(SNAPSHOT_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}

    out = {}
    for i in snap.get("items", []):
        if not isinstance(i, dict):
            continue
        code = str(i.get("code", "")).strip()
        if not code:
            continue
        gsz = d(i.get("gsz", "0"))
        dwjz = d(i.get("dwjz", "0"))
        out[code] = gsz - dwjz
    return out


def load_today_operations() -> str:
    if not RECEIPT_JSON.exists():
        return "无"
    try:
        rc = json.loads(RECEIPT_JSON.read_text(encoding="utf-8"))
    except Exception:
        return "无"

    if not rc.get("confirmed", False):
        return "无"

    executed = str(rc.get("executedAt", ""))
    if today() not in executed:
        return "无"

    action_type = str(rc.get("actionType", "")).upper() or "UNKNOWN"
    code = ""
    patch = rc.get("holdingsPatch")
    if isinstance(patch, list) and patch:
        code = str((patch[0] or {}).get("code", ""))

    if action_type == "BUY":
        action_zh = "买入"
    elif action_type in {"REDEEM", "SELL"}:
        action_zh = "卖出"
    else:
        action_zh = action_type

    raw = str(rc.get("rawText", "")).strip()
    details = raw if raw else f"{action_zh} {code}".strip()
    return details or "无"


def build_update_report() -> str:
    line = status_line()
    m = parse_status_metrics(line)

    if not STATE_JSON.exists():
        return f"更新成功（摘要）\n- 组合净值(PV)：{m['PV']}\n- 总盈亏(UPnL)：{m['UPnL']}\n- 距目标(Gap)：{m['Gap']}\n- 今日操作：{load_today_operations()}"

    state = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    holdings = state.get("holdings", []) if isinstance(state, dict) else []
    nav_delta = load_snapshot_today_pnl_map()

    lines = [
        f"更新成功（{today()}）",
        f"- 组合净值(PV)：{m['PV']}",
        f"- 总盈亏(UPnL)：{m['UPnL']}",
        f"- 距目标(Gap)：{m['Gap']}",
        f"- 今日操作：{load_today_operations()}",
        "- 持仓明细：",
    ]

    for h in holdings:
        code = str(h.get("code", ""))
        name = str(h.get("name", ""))
        shares = str(h.get("shares", h.get("totalShares", "0")))
        hold_pnl = str(h.get("unrealizedPnl", "0"))
        hold_amount = str(h.get("marketValue", "0"))

        today_unit_delta = d(nav_delta.get(code, "0"))
        today_pnl = q2(d(shares, "0") * today_unit_delta)

        lines.append(
            f"  - {code} {name}｜持仓金额:{hold_amount}元｜今日盈亏:{today_pnl}｜持仓盈亏:{hold_pnl}"
        )

    return "\n".join(lines)


def handle_attempt(state: dict, is_init: bool) -> str:
    ok, msg = try_refresh()
    if ok:
        state.update({"active": False, "completed": True, "success": True, "lastError": ""})
        save_state(state)
        return build_update_report()

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
