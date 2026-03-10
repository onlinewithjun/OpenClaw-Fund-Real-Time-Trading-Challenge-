from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from urllib.request import urlopen


def to_decimal(v: object, default: str = "0") -> Decimal:
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def q2(v: Decimal) -> str:
    return str(v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fetch_gz(code: str, timeout: int = 10) -> dict:
    # Eastmoney/Tiantian gz endpoint (jsonp)
    url = f"https://fundgz.1234567.com.cn/js/{code}.js?rt={int(time.time()*1000)}"
    with urlopen(url, timeout=timeout) as resp:
        text = resp.read().decode("utf-8", errors="ignore")
    m = re.search(r"\{.*\}", text)
    if not m:
        raise RuntimeError(f"invalid_gz_payload:{code}")
    return json.loads(m.group(0))


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch nav snapshot and write fund_challenge/nav_snapshot.json")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--out", default="fund_challenge/nav_snapshot.json")
    args = ap.parse_args()

    state_path = Path(args.state)
    out_path = Path(args.out)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    items = []

    for h in state.get("holdings", []):
        code = str(h.get("code", "")).strip()
        name = str(h.get("name", "")).strip()
        old_mv = to_decimal(h.get("marketValue", "0"))
        old_upnl = to_decimal(h.get("unrealizedPnl", "0"))

        if not code:
            continue

        gz = fetch_gz(code)
        dwjz = to_decimal(gz.get("dwjz", "0"))
        gsz = to_decimal(gz.get("gsz", "0"))

        # Prefer gsz when available (>0), fallback dwjz.
        nav_new = gsz if gsz > 0 else dwjz
        nav_base = dwjz if dwjz > 0 else nav_new
        ratio = (nav_new / nav_base) if nav_base > 0 else Decimal("1")

        new_mv = (old_mv * ratio)
        delta = new_mv - old_mv
        new_upnl = old_upnl + delta

        items.append({
            "code": code,
            "name": name,
            "marketValue": q2(new_mv),
            "unrealizedPnl": q2(new_upnl),
            "source": "fundgz.1234567.com.cn",
            "dwjz": str(dwjz),
            "gsz": str(gsz),
            "gztime": str(gz.get("gztime", "")),
        })

    payload = {
        "asOf": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": "eastmoney_fundgz",
        "items": items,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"NAV_SNAPSHOT_OK items={len(items)} asOf={payload['asOf']}")


if __name__ == "__main__":
    main()
