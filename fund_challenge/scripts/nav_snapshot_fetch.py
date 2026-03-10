from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen


def fetch_gz(code: str, timeout: int = 10) -> dict:
    url = f"https://fundgz.1234567.com.cn/js/{code}.js?rt={int(time.time()*1000)}"
    with urlopen(url, timeout=timeout) as resp:
        text = resp.read().decode("utf-8", errors="ignore")
    m = re.search(r"\{.*\}", text)
    if not m:
        raise RuntimeError(f"invalid_gz_payload:{code}")
    return json.loads(m.group(0))


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch NAV snapshot only (no PnL math)")
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
        if not code:
            continue
        gz = fetch_gz(code)
        dwjz = str(gz.get("dwjz", ""))
        gsz = str(gz.get("gsz", ""))
        nav = gsz if gsz not in ("", "0", "0.0000") else dwjz
        if not nav:
            raise RuntimeError(f"empty_nav:{code}")
        items.append(
            {
                "code": code,
                "name": name,
                "nav": nav,
                "dwjz": dwjz,
                "gsz": gsz,
                "gztime": str(gz.get("gztime", "")),
                "source": "fundgz.1234567.com.cn",
            }
        )

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
