#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
UNIVERSE_DIR = WORKSPACE / "fund_challenge" / "universe"
JSON_PATH = UNIVERSE_DIR / "daily_candidates.json"

# Broad universe (>=50) for online scan
BROAD_CODES = [
    "510300", "510500", "159915", "159949", "588000", "512480", "159995", "159967", "512170", "515000",
    "512100", "515880", "159819", "159857", "159928", "159939", "159996", "512010", "515790", "512690",
    "159825", "159902", "159934", "518800", "518880", "159980", "513100", "513500", "159941", "513050",
    "513330", "513180", "159509", "159740", "512660", "515220", "515170", "516160", "516110", "159611",
    "159766", "159755", "159870", "159760", "159778", "159845", "159865", "159822", "159766", "159881",
    "001938", "017192", "020899", "002611", "000001", "000011", "000021", "000056", "000061", "001245",
]

GOLD_CODES = {"518800", "518880", "159934", "002611", "159980"}
BROAD_INDEX_CODES = {"510300", "510500", "159915", "159949", "588000"}
TECH_CODES = {"159995", "512480", "159967", "513100", "513050", "513330", "159509", "019118", "020899"}
CYCLICAL_CODES = {"017192", "159870", "159822", "159881", "512100", "515880", "000056"}

# 场内代理代码 -> 场外可申购代码（挑战账户执行口径）
CODE_REMAP: dict[str, tuple[str, str]] = {
    "159509": ("019118", "景顺长城纳斯达克科技ETF(QDII)E人民币"),
}


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


def main() -> None:
    started = now_cn_iso()

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

    if len(scan_rows) < 20:
        fail(f"online_scan_insufficient success={len(scan_rows)}")

    # upgraded refine score: momentum + stability + persistence - noise
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

        score = 1.2 * momentum + 0.45 * persistence + 0.40 * stability - 0.25 * noise_penalty
        scored_rows.append({**r, "score": score, "stability": stability, "persistence": persistence, "delta": delta})

    scored_rows.sort(key=lambda x: x["score"], reverse=True)

    refined: list[dict] = []
    selected_codes: set[str] = set()
    cap = {"tech_growth": 4, "cyclical_resources": 3, "gold_defensive": 2, "broad_index_core": 4}
    used = {k: 0 for k in cap}

    for r in scored_rows:
        src_code = r["code"]
        mapped_code, mapped_name = CODE_REMAP.get(src_code, (src_code, r["name"]))

        cat = categorize(mapped_code)
        if used[cat] >= cap[cat]:
            continue
        if mapped_code in selected_codes:
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

    if len(refined) < 8:
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
