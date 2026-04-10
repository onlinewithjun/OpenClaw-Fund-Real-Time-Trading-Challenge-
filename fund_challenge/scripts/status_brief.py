from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

from state_math import compute


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_gszzl(rationale: str) -> float:
    """从 rationale 中提取 gszzl 预估涨幅"""
    m = re.search(r"gszzl=([\-0-9.]+)%", str(rationale))
    return float(m.group(1)) if m else 0.0


def extract_score(rationale: str) -> float:
    """从 rationale 中提取 strategy score"""
    m = re.search(r"score=([\-0-9.]+)", str(rationale))
    return float(m.group(1)) if m else 0.0


def recent_redeem_codes(days: int = 3) -> set[str]:
    ledger = Path("fund_challenge/ledger.jsonl")
    if not ledger.exists():
        return set()
    cutoff = datetime.now() - timedelta(days=days)
    out: set[str] = set()
    for raw in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.replace("\x00", "").strip()
        if not line.startswith("{"):
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        if str(item.get("event", "")) != "execution_confirmed":
            continue
        if str(item.get("actionType", "")).upper() not in {"REDEEM", "SELL"}:
            continue
        code = str(item.get("code", "")).strip()
        if not code:
            note = str(item.get("note", ""))
            m = re.search(r"sold\s+(\d{6})", note)
            if m:
                code = m.group(1)
        ts = str(item.get("ts", "")).replace("Z", "+00:00")
        if not code or not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if dt >= cutoff:
            out.add(code)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate compact challenge status line")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--candidates", default="fund_challenge/universe/daily_candidates.json")
    ap.add_argument("--max-holdings", type=int, default=3)
    args = ap.parse_args()

    state = load_json(Path(args.state))
    digest = compute(state)
    holdings = state.get("holdings", [])[: args.max_holdings]
    
    # 加载候选基金池
    candidates_data = load_json(Path(args.candidates)) if Path(args.candidates).exists() else {}
    candidates = candidates_data.get("candidates", [])

    # 构建持仓代码集合
    holding_codes = {str(h.get("code", "")) for h in state.get("holdings", [])}

    # 为每个候选基金添加持仓标记和排序键
    enriched_candidates = []
    for c in candidates:
        code = str(c.get("code", ""))
        confidence = float(c.get("confidence", "0"))
        gszzl = extract_gszzl(c.get("rationale", ""))
        in_portfolio = code in holding_codes
        score = extract_score(c.get("rationale", ""))
        # 排序键：strategy score 优先，其次置信度，再次预估涨幅
        sort_key = (score, confidence, gszzl)
        enriched_candidates.append({
            "code": code,
            "name": c.get("name", ""),
            "confidence": confidence,
            "gszzl": gszzl,
            "category": c.get("category", ""),
            "in_portfolio": in_portfolio,
            "sort_key": sort_key,
        })

    # 按 strategy score、置信度、预估涨幅降序排序
    enriched_candidates.sort(key=lambda x: x["sort_key"], reverse=True)

    pending = state.get("pendingTransactions", []) if isinstance(state, dict) else []
    active_pending = [
        t for t in pending
        if str((t or {}).get("status", "")).upper() not in {"SETTLED", "CANCELLED", "FAILED"}
        and not str((t or {}).get("resolvedAt", "")).strip()
    ]

    parts = [
        f"PV {digest['portfolioValue']}",
        f"UPnL {digest['totalUnrealizedPnl']}",
        f"Gap {digest['distanceToTarget']}",
    ]

    pending_buy = [t for t in active_pending if str((t or {}).get("actionType", "")).upper() == "BUY"]
    pending_redeem = [t for t in active_pending if str((t or {}).get("actionType", "")).upper() in {"REDEEM", "SELL"}]

    if pending_buy:
        parts.append(f"PendingBUY {len(pending_buy)}")
    elif pending_redeem:
        parts.append(f"PendingREDEEM {len(pending_redeem)}")

    # 输出持仓基金表现
    for h in holdings:
        code = h.get("code", "?")
        pnl = h.get("unrealizedPnl", "?")
        parts.append(f"{code}:{pnl}")

    # 输出全池子候选排名（Top 5）
    top_candidates = enriched_candidates[:5]
    candidate_signals = []
    for c in top_candidates:
        marker = "H" if c["in_portfolio"] else "N"  # H=持仓中，N=新候选
        sign = "+" if c["gszzl"] >= 0 else ""
        candidate_signals.append(f"{c['code']}({marker}):{sign}{c['gszzl']:.2f}%@{c['confidence']:.2f}")
    
    parts.append(f"Candidates[{len(enriched_candidates)}]: " + " | ".join(candidate_signals))

    # 生成调仓建议
    recent_redeems = recent_redeem_codes(days=3)
    # 找出最佳新候选（未持仓、信号为正、且不是刚卖出的低质量回补）
    best_new = next((c for c in enriched_candidates if not c["in_portfolio"] and c["gszzl"] > 0 and c["code"] not in recent_redeems), None)
    # 找出最差持仓（持仓中且信号为负）
    worst_holding = next((c for c in enriched_candidates if c["in_portfolio"] and c["gszzl"] < 0), None)
    
    if pending_buy:
        parts.append("Suggestion: HOLD_PENDING_BUY_SETTLEMENT")
    elif pending_redeem:
        parts.append("Suggestion: REDEEM_PENDING_CASH_STILL_USABLE")
    elif best_new and worst_holding:
        parts.append(f"Suggestion: REDUCE {worst_holding['code']} -> ADD {best_new['code']}")
    elif best_new:
        parts.append(f"Suggestion: ADD {best_new['code']}")
    elif worst_holding:
        parts.append(f"Suggestion: REDUCE {worst_holding['code']}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
