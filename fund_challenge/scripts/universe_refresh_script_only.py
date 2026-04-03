#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
UNIVERSE_DIR = WORKSPACE / "fund_challenge" / "universe"
JSON_PATH = UNIVERSE_DIR / "daily_candidates.json"

# Broad universe (expanded to ~120) for online scan
# Focus on actively traded funds with reliable data feeds
BROAD_CODES = [
    # === 现有核心候选 (Keep existing) ===
    "020899", "017192", "002611", "000061", "001245", "000021", "000011", "000056",
    # === 科技/AI/通信 (Tech/AI) - 热门主动基金 ===
    "000063", "000066", "000069", "000073", "000082", "000190", "000191", "000220", "000251", "000263",
    "000270", "000279", "000294", "000311", "000326", "000327", "000363", "000368", "000371", "000376",
    "000478", "000512", "000519", "000524", "000535", "000592", "000612", "000628", "000634", "000656",
    "000696", "000711", "000751", "000762", "000780", "000793", "000822", "000866", "000893", "000925",
    "000955", "000961", "000991", "001001", "001008", "001011", "001028", "001042", "001053", "001069",
    "001071", "001112", "001117", "001144", "001158", "001171", "001180", "001182", "001186", "001188",
    "001193", "001210", "001220", "001236", "001242", "001267", "001270", "001313", "001316", "001323",
    "001349", "001373", "001396", "001410", "001426", "001437", "001463", "001475", "001495", "001512",
    "001513", "001521", "001524", "001536", "001549", "001559", "001577", "001593", "001605", "001617",
    "001620", "001630", "001644", "001656", "001665", "001679", "001694", "001717", "001720", "001733",
    "001744", "001751", "001766", "001809", "001815", "001832", "001837", "001838", "001849", "001863",
    "001869", "001880", "001909", "001917", "001965", "001983", "001995", "002001", "002031",
    # === 周期/资源 (Cyclical/Resources) ===
    "001719", "001720", "002610", "002612", "002613", "002614",
    # === 消费 (Consumer) ===
    "000072", "000083", "000110", "000120", "000121", "000123", "000124", "000125",
    # === 医药 (Healthcare) ===
    "000171", "000173", "000174", "000175", "000176", "000177", "000178", "000179", "000180", "000181",
    # === QDII (US/HK) ===
    "000041", "000042", "000043", "000044", "000045", "000046", "000047", "000048", "000049", "000050",
    "000051", "000052", "000053", "000054", "000055", "000057", "000058", "000059", "000060", "000062",
    "000068", "000071", "000075", "000076", "000077", "000078", "000079", "000080", "000081",
    "001911", "001918",
]

GOLD_CODES = {"518800", "518880", "159934", "002611", "159980"}
BROAD_INDEX_CODES = {"510300", "510500", "159915", "159949", "588000"}
TECH_CODES = {"159995", "512480", "159967", "513100", "513050", "513330", "020899"}
CYCLICAL_CODES = {"017192", "159870", "159822", "159881", "512100", "515880", "000056"}

# 场内代理代码 -> 场外可申购代码（挑战账户执行口径）
# 2026-04-03: keep empty unless the off-exchange mapped code is explicitly confirmed
# purchasable on Alipay. This prevents stale proxy mappings from reintroducing blocked funds.
CODE_REMAP: dict[str, tuple[str, str]] = {}


def is_off_exchange_candidate(code: str, name: str) -> bool:
    # 挑战账户执行口径：仅保留可在支付宝/天天基金直接申购的场外基金。
    # 目前采用保守规则：仅保留 0 开头基金代码（含 000/001/002/017/019/020 等）。
    return str(code).startswith("0")


def fail(msg: str) -> None:
    print(f"UNIVERSE_REFRESH_ALERT: {msg}")
    raise SystemExit(1)


def now_cn_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def to_float(v: str, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def fetch_one(code: str, timeout: float = 4.0) -> dict | None:
    url = f"https://fundgz.1234567.com.cn/js/{code}.js?rt={int(time.time()*1000)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            txt = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return None

    m = re.search(r"\((\{.*\})\)", txt)
    if not m:
        return None
    try:
        d = json.loads(m.group(1))
    except Exception:
        return None

    name = str(d.get("name") or "").strip()
    if not name:
        return None

    gszzl = to_float(str(d.get("gszzl", "0")))
    gsz = str(d.get("gsz") or d.get("dwjz") or "")
    return {
        "code": code,
        "name": name,
        "gszzl": gszzl,
        "gsz": gsz,
        "sourceUrl": f"https://fundf10.eastmoney.com/{code}.html",
    }


def categorize(code: str) -> str:
    if code in GOLD_CODES:
        return "gold_defensive"
    if code in BROAD_INDEX_CODES:
        return "broad_index_core"
    if code in TECH_CODES:
        return "tech_growth"
    if code in CYCLICAL_CODES:
        return "cyclical_resources"
    return "broad_index_core"


CATEGORY_SCORE_BIAS = {
    "tech_growth": 0.18,
    "cyclical_resources": 0.08,
    "gold_defensive": 0.02,
    "broad_index_core": -0.10,
}


def confidence_from_score(score: float) -> float:
    # map composite score (roughly 0-2.5) to [0.70, 0.95]
    conf = 0.70 + min(max(score, 0.0), 2.5) * 0.10
    return round(min(conf, 0.95), 2)


def build_prev_maps(path: Path) -> tuple[dict[str, float], dict[str, float], dict[str, str]]:
    prev_conf: dict[str, float] = {}
    prev_mom: dict[str, float] = {}
    prev_name: dict[str, str] = {}
    if not path.exists():
        return prev_conf, prev_mom, prev_name
    try:
        old = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return prev_conf, prev_mom, prev_name

    for c in old.get("candidates", []):
        if not isinstance(c, dict):
            continue
        code = str(c.get("code", "")).strip()
        if not code:
            continue
        prev_name[code] = str(c.get("name", "")).strip()
        prev_conf[code] = to_float(str(c.get("confidence", "0")))
        # try to recover last momentum from rationale text if present
        m = re.search(r"gszzl=([\-0-9.]+)%", str(c.get("rationale", "")))
        if m:
            prev_mom[code] = to_float(m.group(1))
    return prev_conf, prev_mom, prev_name


def ensure_today_mtime(path: Path) -> None:
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    if mtime.date() != datetime.now().date():
        fail(f"json mtime not today: {mtime.isoformat()}")


def load_alipay_allowed() -> set[str]:
    """Load user-confirmed Alipay-purchasable fund codes."""
    allowed_path = UNIVERSE_DIR / "alipay_allowed.json"
    if not allowed_path.exists():
        return set()
    try:
        data = json.loads(allowed_path.read_text(encoding="utf-8"))
        return {str(item["code"]) for item in data.get("allowed", []) if isinstance(item, dict)}
    except Exception:
        return set()

def load_user_holdings() -> set[str]:
    """Load current challenge-account holdings from canonical state first."""
    codes = set()

    state_path = WORKSPACE / "fund_challenge" / "state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            for item in state.get("holdings", []):
                code = str(item.get("code", "")).strip()
                shares = to_float(str(item.get("totalShares", item.get("shares", "0"))))
                if code and shares > 0:
                    codes.add(code)
        except Exception:
            pass

    if codes:
        return codes

    # Fallback only: try holdings.csv if canonical challenge state is unavailable.
    holdings_path = WORKSPACE / "holdings.csv"
    if holdings_path.exists():
        try:
            import csv
            for enc in ["utf-8-sig", "gbk", "utf-8"]:
                try:
                    with open(holdings_path, "r", encoding=enc) as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            code = str(row.get("代码", row.get("code", ""))).strip()
                            if code and code.isdigit():
                                codes.add(code)
                    break
                except UnicodeDecodeError:
                    continue
        except Exception:
            pass

    return codes


def load_recent_redeems(cooldown_days: int = 2) -> set[str]:
    ledger_path = WORKSPACE / "fund_challenge" / "ledger.jsonl"
    if not ledger_path.exists():
        return set()

    cutoff = datetime.now() - timedelta(days=cooldown_days)
    out: set[str] = set()
    try:
        for raw in ledger_path.read_text(encoding="utf-8", errors="ignore").splitlines():
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
                continue
            ts = str(item.get("ts", "")).replace("Z", "+00:00")
            try:
                dt = datetime.fromisoformat(ts)
            except Exception:
                continue
            if dt >= cutoff:
                out.add(code)
    except Exception:
        return set()
    return out


def main() -> None:
    started = now_cn_iso()

    alipay_allowed = load_alipay_allowed()
    user_holdings = load_user_holdings()
    recent_redeems = load_recent_redeems(cooldown_days=2)
    prev_codes: set[str] = set()
    prev_conf_map, prev_mom_map, prev_name_map = build_prev_maps(JSON_PATH)
    if JSON_PATH.exists():
        try:
            old = json.loads(JSON_PATH.read_text(encoding="utf-8"))
            for c in old.get("candidates", []):
                if isinstance(c, dict):
                    prev_codes.add(str(c.get("code", "")))
        except Exception:
            pass

    scan_rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(fetch_one, code): code for code in BROAD_CODES}
        for f in as_completed(futures):
            row = f.result()
            if row:
                scan_rows.append(row)

    if len(scan_rows) < 10:
        fail(f"online_scan_insufficient success={len(scan_rows)}")

    # upgraded refine score: momentum + stability + persistence - noise
    # Reduced persistence weight from 0.45 to 0.20 for better new fund discovery
    scored_rows: list[dict] = []
    for r in scan_rows:
        code = r["code"]
        mom = float(r["gszzl"])
        prev_mom = float(prev_mom_map.get(code, mom))
        delta = abs(mom - prev_mom)

        momentum = max(min(mom / 3.0, 1.0), -1.0)  # [-1,1]
        persistence = 1.0 if code in prev_codes else 0.0
        stability = max(0.0, 1.0 - min(delta / 3.0, 1.0))
        noise_penalty = min(abs(mom) / 6.0, 1.0)

        category = categorize(code)
        category_bias = CATEGORY_SCORE_BIAS.get(category, 0.0)
        score = 1.2 * momentum + 0.20 * persistence + 0.40 * stability - 0.25 * noise_penalty + category_bias
        scored_rows.append({**r, "score": score, "stability": stability, "persistence": persistence, "delta": delta, "category": category})

    scored_rows.sort(key=lambda x: x["score"], reverse=True)

    refined: list[dict] = []
    selected_codes: set[str] = set()
    # Expanded caps for ~50 candidates total
    cap = {"tech_growth": 18, "cyclical_resources": 12, "gold_defensive": 8, "broad_index_core": 12}
    used = {k: 0 for k in cap}

    # Phase 1: Always retain user's current holdings (bypass category caps)
    for r in scored_rows:
        src_code = r["code"]
        mapped_code, mapped_name = CODE_REMAP.get(src_code, (src_code, r["name"]))

        if not is_off_exchange_candidate(mapped_code, mapped_name):
            continue

        # CRITICAL: Always retain user's current holdings
        if mapped_code in user_holdings:
            if mapped_code in selected_codes:
                continue
            selected_codes.add(mapped_code)
            cat = categorize(mapped_code)
            used[cat] += 1

            conf = confidence_from_score(float(r["score"]))
            rationale = (
                f"score={r['score']:.2f}; momentum gszzl={r['gszzl']:.2f}%; "
                f"stability={r['stability']:.2f}; persistence={r['persistence']:.0f}; src={src_code} [HELD]"
            )
            refined.append(
                {
                    "code": mapped_code,
                    "name": mapped_name,
                    "category": cat,
                    "rationale": rationale,
                    "sourceUrl": r["sourceUrl"],
                    "verifiedAt": started,
                    "confidence": f"{conf:.2f}",
                    "purchasableOn": ["tiantianfund", "alipay"],
                    "stage": "deep_refine",
                }
            )

    # Phase 2: Fill remaining slots with top-scored candidates (Alipay-allowed only)
    for r in scored_rows:
        src_code = r["code"]
        mapped_code, mapped_name = CODE_REMAP.get(src_code, (src_code, r["name"]))

        if not is_off_exchange_candidate(mapped_code, mapped_name):
            continue

        # Skip if already selected (holdings phase)
        if mapped_code in selected_codes:
            continue

        # Filter: Only Alipay-allowed funds
        if alipay_allowed and mapped_code not in alipay_allowed:
            continue

        # Avoid low-quality "just sold, immediately buy back" churn unless it is still an actual holding.
        if mapped_code in recent_redeems and mapped_code not in user_holdings:
            continue

        cat = categorize(mapped_code)
        if used[cat] >= cap[cat]:
            continue

        used[cat] += 1
        selected_codes.add(mapped_code)

        conf = confidence_from_score(float(r["score"]))
        rationale = (
            f"score={r['score']:.2f}; momentum gszzl={r['gszzl']:.2f}%; "
            f"stability={r['stability']:.2f}; persistence={r['persistence']:.0f}; src={src_code}"
        )

        refined.append(
            {
                "code": mapped_code,
                "name": mapped_name,
                "category": cat,
                "rationale": rationale,
                "sourceUrl": r["sourceUrl"],
                "verifiedAt": started,
                "confidence": f"{conf:.2f}",
                "purchasableOn": ["tiantianfund", "alipay"],
                "stage": "deep_refine",
            }
        )
        if len(refined) >= 12:
            break

    if len(refined) < 9:
        fail(f"refine_insufficient count={len(refined)}")

    new_codes = {c["code"] for c in refined}
    added = sorted(list(new_codes - prev_codes))
    removed = sorted(list(prev_codes - new_codes))
    retained = sorted(list(prev_codes & new_codes))

    code_to_name = {str(c.get("code", "")): str(c.get("name", "")) for c in refined}

    payload = {
        "updatedAt": started,
        "scanned_count": len(scan_rows),
        "refined_count": len(refined),
        "added": added or ["None"],
        "removed": removed or ["None"],
        "retained": retained or ["None"],
        "candidates": refined,
    }

    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rb = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if "updatedAt" not in rb or not rb.get("candidates"):
        fail("json_readback_failed")
    ensure_today_mtime(JSON_PATH)

    added_desc = "None"
    if added:
        added_desc = ",".join([f"{c}:{code_to_name.get(c, '-') or '-'}" for c in added])

    removed_desc = "None"
    if removed:
        removed_desc = ",".join([f"{c}:{prev_name_map.get(c, '-') or '-'}" for c in removed])

    print(
        f"UNIVERSE_REFRESH_OK json_updatedAt={rb['updatedAt']} "
        f"json_mtime={datetime.fromtimestamp(JSON_PATH.stat().st_mtime).isoformat()} "
        f"scanned={len(scan_rows)} refined={len(refined)} source=online-json "
        f"added={added_desc} removed={removed_desc}"
    )


if __name__ == "__main__":
    main()
