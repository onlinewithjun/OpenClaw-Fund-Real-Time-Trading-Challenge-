from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta, timezone

from state_math import compute
from ttfund_client import fund_base_infos, extract_body

ALIPAY_ALLOWED = Path("fund_challenge/universe/alipay_allowed.json")
MIN_ACTIONABLE_SCORE_EDGE = 0.35
MIN_ACTIONABLE_CONFIDENCE = 0.80
MIN_TRADE_CASH = 20.0


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
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
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
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt >= cutoff:
            out.add(code)
    return out


def _ttfund_base_snapshot(code: str) -> str:
    result = fund_base_infos(code)
    if not result.get("ok"):
        return ""
    body = extract_body(result)
    rows = body.get("data", []) if isinstance(body, dict) else []
    if not rows:
        return ""
    row = rows[0] if isinstance(rows[0], dict) else {}
    risk = str(row.get("RISKLEVEL", "")).strip()
    rate = str(row.get("RATE", "")).strip()
    shortname = str(row.get("SHORTNAME", "")).strip()
    parts = []
    if shortname:
        parts.append(shortname)
    if risk:
        parts.append(f"R{risk}")
    if rate:
        parts.append(f"fee {rate}")
    return ", ".join(parts)


def _normalize_category(raw: str, name: str) -> str:
    title = str(name or "").strip().lower()
    r = str(raw or "").strip()
    if r:
        return r
    mapping = [
        ("gold", ["黄金", "gold"]),
        ("communication", ["通信"]),
        ("resources", ["有色", "金属", "资源", "煤炭"]),
        ("consumer", ["消费", "食品", "家电"]),
        ("manufacturing", ["制造", "工业"]),
        ("broad", ["沪深300", "宽基", "瑞享"]),
    ]
    for k, needles in mapping:
        if any(n.lower() in title for n in needles):
            return k
    return "other"


def load_alipay_allowed_codes() -> set[str]:
    if not ALIPAY_ALLOWED.exists():
        return set()
    try:
        data = load_json(ALIPAY_ALLOWED)
    except Exception:
        return set()
    allowed = data.get("allowed", []) if isinstance(data, dict) else []
    return {
        str(item.get("code", "")).strip()
        for item in allowed
        if isinstance(item, dict) and str(item.get("code", "")).strip()
    }


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

    alipay_allowed_codes = load_alipay_allowed_codes()

    # 为每个候选基金添加持仓标记和排序键
    enriched_candidates = []
    candidate_category_map = {}
    for c in candidates:
        code = str(c.get("code", ""))
        confidence = float(c.get("confidence", "0"))
        gszzl = extract_gszzl(c.get("rationale", ""))
        in_portfolio = code in holding_codes
        score = extract_score(c.get("rationale", ""))
        alipay_allowed = (not alipay_allowed_codes) or (code in alipay_allowed_codes)
        # 排序键：strategy score 优先，其次置信度，再次预估涨幅
        sort_key = (score, confidence, gszzl)
        candidate_category_map[code] = c.get("category", "")
        enriched_candidates.append({
            "code": code,
            "name": c.get("name", ""),
            "confidence": confidence,
            "gszzl": gszzl,
            "score": score,
            "category": c.get("category", ""),
            "in_portfolio": in_portfolio,
            "alipay_allowed": alipay_allowed,
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

    exposure_map = {}
    all_holdings = state.get("holdings", [])
    total_mv = sum(float(h.get("marketValue", 0) or 0) for h in all_holdings) or 0.0
    for h in all_holdings:
        code = str(h.get("code", "")).strip()
        name = str(h.get("name", ""))
        category = _normalize_category(candidate_category_map.get(code, ""), name)
        exposure_map[category] = exposure_map.get(category, 0.0) + float(h.get("marketValue", 0) or 0)
    if exposure_map and total_mv > 0:
        exposure_parts = [f"{k}:{v/total_mv*100:.0f}%" for k, v in sorted(exposure_map.items(), key=lambda x: x[1], reverse=True)]
        parts.append("Exposure " + ", ".join(exposure_parts))

    # 输出持仓基金表现
    for h in holdings:
        code = h.get("code", "?")
        pnl = h.get("unrealizedPnl", "?")
        base = _ttfund_base_snapshot(str(code)) if code and code != "?" else ""
        if base:
            parts.append(f"{code}:{pnl}({base})")
        else:
            parts.append(f"{code}:{pnl}")

    # 输出全池子候选排名（Top 5）
    top_candidates = enriched_candidates[:5]
    candidate_signals = []
    for c in top_candidates:
        marker = "H" if c["in_portfolio"] else "N"  # H=持仓中，N=新候选
        alipay_marker = "A" if c["alipay_allowed"] else "X"
        sign = "+" if c["gszzl"] >= 0 else ""
        candidate_signals.append(f"{c['code']}({marker},{alipay_marker}):s{c['score']:.2f}|{sign}{c['gszzl']:.2f}%@{c['confidence']:.2f}")

    parts.append(f"Candidates[{len(enriched_candidates)}]: " + " | ".join(candidate_signals))

    # 生成调仓建议。这里只输出保守、可执行的建议，不把量化排序直接当交易指令。
    recent_redeems = recent_redeem_codes(days=3)
    actionable_new_candidates = [
        c for c in enriched_candidates
        if (not c["in_portfolio"])
        and c["alipay_allowed"]
        and c["gszzl"] > 0
        and c["confidence"] >= MIN_ACTIONABLE_CONFIDENCE
        and c["code"] not in recent_redeems
    ]
    best_new = actionable_new_candidates[0] if actionable_new_candidates else None

    actionable_held_candidates = [c for c in enriched_candidates if c["in_portfolio"]]
    worst_holding = next((c for c in reversed(actionable_held_candidates) if c["gszzl"] < 0), None)

    cash = float(state.get("cash", 0) or 0)
    score_edge = (best_new["score"] - worst_holding["score"]) if (best_new and worst_holding) else 0.0

    if pending_buy:
        parts.append("Suggestion: HOLD_PENDING_BUY_SETTLEMENT")
    elif pending_redeem and cash < MIN_TRADE_CASH:
        parts.append("Suggestion: HOLD_WAIT_REDEEM_CASH")
    elif pending_redeem:
        parts.append("Suggestion: REDEEM_PENDING_NON_BLOCKING")
    elif best_new and worst_holding and score_edge >= MIN_ACTIONABLE_SCORE_EDGE:
        parts.append(f"Suggestion: REDUCE {worst_holding['code']} -> WATCH/ADD {best_new['code']}")
    elif best_new and cash >= MIN_TRADE_CASH:
        parts.append(f"Suggestion: WATCH/ADD {best_new['code']}")
    elif worst_holding:
        parts.append(f"Suggestion: REVIEW_REDUCE {worst_holding['code']}")
    else:
        parts.append("Suggestion: HOLD_NO_HIGH_EDGE_ROTATION")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
