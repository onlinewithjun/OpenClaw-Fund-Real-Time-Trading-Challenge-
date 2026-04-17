from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OPENCLAW_CONFIG = ROOT.parent / "openclaw.json"
GATEWAY_URL = "https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke"


def _load_key_from_openclaw_json() -> str:
    if not OPENCLAW_CONFIG.exists():
        return ""
    try:
        data = json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return ""
    env = data.get("env", {}) if isinstance(data, dict) else {}
    return str(env.get("TTFUND_APIKEY", "")).strip()


def get_api_key() -> str:
    return str(os.getenv("TTFUND_APIKEY") or _load_key_from_openclaw_json()).strip()


def invoke_skill(skill_id: str, version: str, payload: dict[str, Any], timeout: int = 20) -> dict[str, Any]:
    api_key = get_api_key()
    if not api_key:
        return {"ok": False, "error": "missing_ttfund_apikey"}
    body = {"skill_id": skill_id, "_skill_version": version, **payload}
    req = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"http_{e.code}"}
    except Exception as e:
        return {"ok": False, "error": f"request_failed:{e}"}
    if data.get("code") != 0:
        return {"ok": False, "error": f"gateway_code_{data.get('code')}", "raw": data}
    return {"ok": True, "data": data}


def extract_body(result: dict[str, Any]) -> dict[str, Any]:
    try:
        return result["data"]["data"]["raw_result"]["body"]
    except Exception:
        return {}


def fund_base_infos(fcode: str) -> dict[str, Any]:
    return invoke_skill("FUND_BASE_INFOS", "1.1.0", {"fcode": str(fcode).strip()})


def fund_nav_info(fund_id: str, range_code: str = "n") -> dict[str, Any]:
    return invoke_skill("FUND_NAV_INFO", "1.0.0", {"fund_id": str(fund_id).strip(), "range": range_code})


def fund_holding_info(fund_id: str, holding_type: str = "all") -> dict[str, Any]:
    return invoke_skill("FUND_HOLDING_INFO", "1.0.0", {"fund_id": str(fund_id).strip(), "holding_type": holding_type})


def extract_top_stock_holdings(result: dict[str, Any]) -> list[dict[str, Any]]:
    body = extract_body(result)
    try:
        stocks = body["data"]["top_holdings"]["stock"]
    except Exception:
        return []
    if not isinstance(stocks, list):
        return []
    out: list[dict[str, Any]] = []
    for row in stocks:
        if not isinstance(row, dict):
            continue
        out.append({
            "code": str(row.get("GPDM", "")).strip(),
            "name": str(row.get("GPJC", "")).strip(),
            "weight": str(row.get("JZBL", "")).strip(),
            "sector": str(row.get("INDEXNAME", "")).strip(),
        })
    return out


def compare_fund_overlap(code_a: str, code_b: str) -> dict[str, Any]:
    ra = fund_holding_info(code_a, "all")
    rb = fund_holding_info(code_b, "all")
    if not ra.get("ok") or not rb.get("ok"):
        return {"ok": False, "error": "holding_fetch_failed"}
    ha = extract_top_stock_holdings(ra)
    hb = extract_top_stock_holdings(rb)
    set_a = {x["code"] for x in ha if x.get("code")}
    set_b = {x["code"] for x in hb if x.get("code")}
    inter = sorted(set_a & set_b)
    union = sorted(set_a | set_b)
    ratio = (len(inter) / len(union)) if union else 0.0
    return {
        "ok": True,
        "overlapCount": len(inter),
        "overlapRatio": round(ratio, 4),
        "sharedCodes": inter,
        "aTop": ha,
        "bTop": hb,
    }
