from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from state_math import compute

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "fund_challenge" / "state.json"
LEDGER = ROOT / "fund_challenge" / "ledger.jsonl"


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def sum_float(vals):
    return sum(float(v) for v in vals)


def latest_ops(limit: int = 5) -> list[str]:
    if not LEDGER.exists():
        return []
    lines = [x.strip() for x in LEDGER.read_text(encoding="utf-8", errors="ignore").splitlines() if x.strip()]
    out = []
    for line in lines[-30:]:
        try:
            o = json.loads(line)
        except Exception:
            continue
        ev = str(o.get("event", ""))
        if ev:
            out.append(ev)
    return out[-limit:]


def active_pending_transactions(state: dict) -> list[dict]:
    pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
    out = []
    for t in pending:
        if str(t.get("status", "")).upper() in {"SETTLED", "CANCELLED", "FAILED"}:
            continue
        if str(t.get("resolvedAt", "")).strip():
            continue
        out.append(t)
    return out


def main() -> None:
    s = load_state()
    asof = str(s.get("asOf", ""))
    today = datetime.now().strftime("%Y-%m-%d")
    if not asof.startswith(today):
        active_pending = active_pending_transactions(s)
        pending_codes = [str(t.get("code", "")).strip() for t in active_pending if str(t.get("code", "")).strip()]
        pending_text = "无在途单" if not active_pending else f"在途{len(active_pending)}笔({','.join(pending_codes) or 'UNKNOWN'})"
        print("【基金挑战#07｜21:45总结复盘】 SUMMARY_REVIEW_ALERT: stale_state_data")
        print(f"- 夜间复盘拿到的 state.asOf={asof or 'UNKNOWN'}，不是今天数据；当前只能做系统优化，不能把它当成新交易日有效盘后结论。")
        print(f"- 执行闭环状态：{pending_text}。若仍有未落账 BUY/REDEEM，次日信号应优先让位于确认与结算。")
        return

    hs = s.get("holdings", [])
    cash = float(s.get("cash", "0") or 0)
    mv = sum_float([h.get("marketValue", "0") for h in hs])
    upnl = sum_float([h.get("unrealizedPnl", "0") for h in hs])
    pv = cash + mv
    gap = 2000.0 - pv

    # contributors
    sorted_by_pnl = sorted(hs, key=lambda x: float(x.get("unrealizedPnl", "0")))
    worst = sorted_by_pnl[0] if sorted_by_pnl else {}
    best = sorted_by_pnl[-1] if sorted_by_pnl else {}

    ops = latest_ops()
    active_pending = active_pending_transactions(s)

    print("【基金挑战#07｜21:45总结复盘】 SUMMARY_REVIEW_OK")
    digest = compute(s)
    economic_pv = pv + float(digest.get('pendingBuyAmount', '0') or 0)
    economic_gap = 2000.0 - economic_pv
    print(f"- 组合总览：账面PV {pv:.2f} | 含BUY在途经济PV {economic_pv:.2f} | UPnL {upnl:.2f} | 账面Gap {gap:.2f} | 经济Gap {economic_gap:.2f} | asOf {asof}")
    if float(digest.get('pendingBuyAmount', '0') or 0) > 0 or float(digest.get('pendingRedeemAmount', '0') or 0) > 0:
        print(f"- 在途交易：BUY在途 {digest.get('pendingBuyAmount')} | REDEEM在途 {digest.get('pendingRedeemAmount')}（BUY会先扣现金、确认前未入持仓，故需同时看经济PV）")
    print("- 持仓逐项表现：")
    for h in hs:
        print(
            f"  - {h.get('code','')} {h.get('name','')} | 持仓金额 {float(h.get('marketValue','0')):.2f} | 持仓盈亏 {float(h.get('unrealizedPnl','0')):.2f}"
        )
    print(f"- 贡献结构：最强 {best.get('code','-')}({float(best.get('unrealizedPnl','0') or 0):.2f})，最弱 {worst.get('code','-')}({float(worst.get('unrealizedPnl','0') or 0):.2f})")
    overnight_pending = []
    today = datetime.now().date()
    for t in active_pending:
        created_at = str((t or {}).get("createdAt", "")).strip()
        code = str((t or {}).get("code", "")).strip()
        if not created_at:
            continue
        try:
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except Exception:
            continue
        if created_dt.date() < today:
            overnight_pending.append(code or "UNKNOWN")

    print("- 策略得失：")
    print("  - 有效：分步任务（更新→总结→复盘）后，晚间链路稳定性提升。")
    print("  - 不足：仓位集中度仍偏高，单品种波动会放大组合回撤。")
    print("  - 硬目标检查：今晚复盘必须回答“当前策略是否提高了 2026-09-04 前把 1000 做到 2000 的概率”。")
    print("  - 方法约束：不迷信禁止追涨/杀跌；只禁止低质量来回打脸交易。")
    if overnight_pending:
        print(f"  - 核心瓶颈：隔夜在途单 {len(overnight_pending)} 笔（{','.join(overnight_pending)}），执行闭环仍慢于信号生成。")
    elif active_pending:
        print(f"  - 核心瓶颈：当前仍有在途单 {len(active_pending)} 笔，新的 BUY/REDEEM 需继续让位于落账确认。")
    if ops:
        print("- 当日关键流水：" + "、".join(ops[-3:]))
    print("- 次日可执行观察清单：")
    watch = [
        "017192 是否继续弱于组合均值，若是则维持降权",
        "020899 强势是否延续，若冲高回落则控制追涨",
        "002611 对冲效果是否改善，评估防守仓位占比",
        "组合现金占比是否满足次日机动仓需求",
        "14:20 state_refresh 是否当日有效（asOf 校验）",
    ]
    for w in watch:
        print(f"  - {w}")


if __name__ == "__main__":
    main()
