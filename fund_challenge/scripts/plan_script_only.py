#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, time, date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]

# 中国2026年主要节日（A股休市日）
CHINA_HOLIDAYS_2026 = [
    # 元旦
    date(2026, 1, 1),
    # 春节（2月15日-2月21日，共7天）
    date(2026, 2, 15), date(2026, 2, 16), date(2026, 2, 17),
    date(2026, 2, 18), date(2026, 2, 19), date(2026, 2, 20), date(2026, 2, 21),
    # 清明节（4月4日-4月6日）
    date(2026, 4, 4), date(2026, 4, 5), date(2026, 4, 6),
    # 劳动节（5月1日-5月5日）
    date(2026, 5, 1), date(2026, 5, 2), date(2026, 5, 3), date(2026, 5, 4), date(2026, 5, 5),
    # 端午节（5月31日）
    date(2026, 5, 31),
    # 中秋节+国庆节（10月1日-10月8日）
    date(2026, 10, 1), date(2026, 10, 2), date(2026, 10, 3),
    date(2026, 10, 4), date(2026, 10, 5), date(2026, 10, 6),
    date(2026, 10, 7), date(2026, 10, 8),
]


def is_trading_day() -> bool:
    """检查今天是否为A股交易日"""
    today = datetime.now().date()
    
    # 检查是否周末
    if today.weekday() >= 5:  # 周六=5，周日=6
        return False
    
    # 检查是否法定节假日
    if today in CHINA_HOLIDAYS_2026:
        return False
    
    return True


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(WORKSPACE), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        return {}


def fail(msg: str) -> None:
    print(f"DECISION_ABORTED_UNVERIFIED_DATA HOLD # {msg}")
    raise SystemExit(1)


def ensure_candidates_fresh_today() -> None:
    p = WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json"
    if not p.exists():
        fail("daily_candidates_missing")

    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        fail("daily_candidates_invalid_json")

    updated = str(d.get("updatedAt", ""))
    if not updated:
        fail("daily_candidates_missing_updatedAt")

    try:
        dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
    except Exception:
        fail(f"daily_candidates_bad_updatedAt {updated}")

    now = datetime.now()
    if dt.date() != now.date():
        fail(f"stale_candidates_date {updated} != {now.date().isoformat()}")

    # Hard business guard: 14:00 plan must consume the 13:35 refresh result.
    # If 13:35 refresh failed, this window check blocks PLAN and raises alert.
    if dt.time() < time(13, 35):
        fail(f"stale_candidates_window updatedAt={updated} before 13:35")


def extract_gszzl(rationale: str) -> float:
    """从 rationale 中提取 gszzl 预估涨幅"""
    m = re.search(r"gszzl=([\-0-9.]+)%", str(rationale))
    return float(m.group(1)) if m else 0.0


def extract_score(rationale: str) -> float:
    m = re.search(r"score=([\-0-9.]+)", str(rationale))
    return float(m.group(1)) if m else 0.0


def generate_full_plan_report(evidence: dict, candidates_data: dict, state: dict) -> str:
    """Generate full plan report (ASCII only for Windows compatibility)"""
    holdings = state.get("holdings", [])
    holding_codes = {str(h.get("code", "")) for h in holdings}
    
    candidates = candidates_data.get("candidates", [])
    enriched = []
    for c in candidates:
        code = str(c.get("code", ""))
        confidence = float(c.get("confidence", "0"))
        gszzl = extract_gszzl(c.get("rationale", ""))
        score = extract_score(c.get("rationale", ""))
        in_portfolio = code in holding_codes
        enriched.append({
            "code": code,
            "name": c.get("name", ""),
            "confidence": confidence,
            "gszzl": gszzl,
            "score": score,
            "category": c.get("category", ""),
            "in_portfolio": in_portfolio,
        })
    
    # Sort by strategy score first, then confidence, then intraday move.
    enriched.sort(key=lambda x: (x["score"], x["confidence"], x["gszzl"]), reverse=True)
    
    # Build rank map for deviation check
    rank_map = {c["code"]: i + 1 for i, c in enumerate(enriched)}
    
    # Generate holding performance lines
    holding_lines = []
    deviation_alerts: list[str] = []
    for h in holdings:
        code = h.get("code", "?")
        pnl = float(h.get("unrealizedPnl", 0) or 0)
        mv = float(h.get("marketValue", 0) or 0)
        marker = "H" if str(code) in holding_codes else " "
        rank = rank_map.get(str(code), None)
        rank_str = f"(rank #{rank})" if rank is not None else ""
        holding_lines.append(f"- {code}({marker}): {mv:.2f} | PnL {pnl:.2f} {rank_str}")
        # Bug 3 fix: flag holdings with quant rank >= 8 as signal deviation
        if rank is not None and rank >= 8:
            deviation_alerts.append(
                f"ALERT: {code} is ranked #{rank} (quant signal weak) but still held - review for reduction or exit"
            )
    
    # Generate full candidate ranking (all refined names, not just Top5)
    candidate_lines = []
    for i, c in enumerate(enriched, 1):
        marker = "H" if c["in_portfolio"] else "N"
        sign = "+" if c["gszzl"] >= 0 else ""
        candidate_lines.append(f"{i}. {c['code']}({marker}): score {c['score']:.2f} | {sign}{c['gszzl']:.2f}% @ {c['confidence']:.2f}")
    
    # Quant-only ranking should be treated as watchlist input, not as a standalone trade trigger.
    best_new = next((c for c in enriched if not c["in_portfolio"] and -3.5 <= c["gszzl"] <= -0.8), None)
    worst_holding = next((c for c in reversed(enriched) if c["in_portfolio"]), None)

    watch_items = []
    if best_new:
        watch_items.append(f"watch pullback {best_new['code']}")
    if worst_holding:
        watch_items.append(f"review trim {worst_holding['code']}")
    suggestion = "WATCHLIST: " + " | ".join(watch_items) if watch_items else "WATCHLIST: HOLD"

    # Generate report
    gs = evidence.get("gateScoring", {})
    risk_switch = gs.get("riskSwitchComputed", "neutral")
    portfolio_value = float(gs.get("inputs", {}).get("portfolioValue", "0"))
    total_upnl = float(gs.get("inputs", {}).get("totalUnrealizedPnl", "0"))
    drawdown = float(gs.get("inputs", {}).get("drawdownPct", "0"))
    target = float((state.get("challenge", {}).get("targetValue", "2000") or "2000"))
    
    lines: list[str] = [
        "[14:00 Plan Report]",
        "",
        "[Framework]",
        "  Macro 30% | Sentiment 25% | Sector 25% | Quant 20%",
        "  Quant ranking below is validation input, not a standalone trade order.",
        "",
        "[Portfolio]",
        f"  PV: {portfolio_value:.2f} | UPnL: {total_upnl:.2f} | DD: {drawdown:.2f}% | Risk: {risk_switch}",
    ]
    
    # Bug 5 fix: PV reaching target -> de-risk alert
    if portfolio_value >= target:
        distance = portfolio_value - target
        lines.append(f"  TARGET REACHED! PV={portfolio_value:.2f} >= {target:.2f} (+{distance:.2f} above target)")
        lines.append("  ** DE-RISK RECOMMENDED: Strongly consider REDEEMING profits rather than initiating new BUYs **")
    
    lines += [
        "",
        "[Holdings]",
    ] + holding_lines + [
        "",
        "[Candidates Full Ranking]",
    ] + candidate_lines + [
        "",
        f"[Action] {suggestion}",
    ]
    
    # Bug 3 fix: append deviation alerts
    if deviation_alerts:
        lines += ["", "[Signal Deviation Alerts]"] + deviation_alerts
    
    return "\n".join(lines)


def main() -> None:
    # Check if today is a trading day (Chinese A-shares)
    if not is_trading_day():
        print("[14:00 Plan Report]")
        print("")
        print("[Holiday Alert]")
        print("  Today is NOT a trading day (Chinese A-shares holiday)")
        print("  No trading plan will be generated.")
        print("")
        print("[Action] SUGGEST: HOLD (Market Closed)")
        return
    
    ensure_candidates_fresh_today()

    code, out, err = run([
        sys.executable,
        "fund_challenge/scripts/preflight_guard.py",
        "--phase",
        "PLAN_ONLY",
        "--workspace",
        ".",
    ])
    if code != 0:
        fail(f"preflight_failed {err[:120]}")

    preflight = parse_json(out)
    if not preflight.get("ok"):
        fail("preflight_not_ok")

    validate = None
    for step in preflight.get("steps", []):
        if step.get("step") == "validate_evidence":
            validate = parse_json(step.get("stdout", ""))
            break

    if not validate:
        fail("validate_missing")

    if validate.get("ok") is not True:
        fail("validate_failed")

    status = str(validate.get("status", "UNKNOWN"))

    code2, out2, err2 = run([sys.executable, "fund_challenge/scripts/status_brief.py"])
    if code2 != 0:
        fail(f"status_brief_failed {err2[:120]}")

    # PLAN_ONLY phase should not be forced to HOLD by status=PENDING_EVIDENCE.
    # Use gate scoring from latest evidence to produce an aggressive-but-guarded plan signal.
    try:
        evidence = json.loads((WORKSPACE / "fund_challenge" / "evidence" / "latest.json").read_text(encoding="utf-8"))
    except Exception:
        print(f"PLAN_ONLY HOLD | status={status} | {out2}")
        return

    # 加载候选基金数据和状态
    try:
        candidates_data = json.loads((WORKSPACE / "fund_challenge" / "universe" / "daily_candidates.json").read_text(encoding="utf-8"))
        state = json.loads((WORKSPACE / "fund_challenge" / "state.json").read_text(encoding="utf-8"))
    except Exception:
        candidates_data = {}
        state = {}

    gs = evidence.get("gateScoring", {}) if isinstance(evidence, dict) else {}
    entry_hint = ((gs.get("entryConsensus") or {}).get("actionHint") if isinstance(gs, dict) else None) or "HOLD"
    exit_hint = ((gs.get("exitConsensus") or {}).get("actionHint") if isinstance(gs, dict) else None) or "HOLD"
    risk_switch = str(gs.get("riskSwitchComputed", "neutral")) if isinstance(gs, dict) else "neutral"

    # 生成完整报告并输出
    full_report = generate_full_plan_report(evidence, candidates_data, state)
    
    # 输出到 stdout 供 Telegram 推送
    if exit_hint == "REDEEM_REDUCE_ALLOWED":
        print(f"PLAN_ONLY REDUCE_READY | risk={risk_switch} | status={status}")
        print(full_report)
        return

    if entry_hint == "TRIAL_BUY_ALLOWED":
        print(f"PLAN_ONLY AGGRESSIVE_BUY_READY | risk={risk_switch} | status={status}")
        print(full_report)
        return

    print(f"PLAN_ONLY HOLD | risk={risk_switch} | status={status}")
    print(full_report)


if __name__ == "__main__":
    main()
