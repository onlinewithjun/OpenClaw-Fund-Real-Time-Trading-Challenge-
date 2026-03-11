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

        # 业务规则：净值优先（dwjz），若净值不可用再降级用估值（gsz）
        if dwjz not in ("", "0", "0.0000"):
            nav = dwjz
            nav_basis = "dwjz"
        elif gsz not in ("", "0", "0.0000"):
            nav = gsz
            nav_basis = "gsz_fallback"
        else:
            raise RuntimeError(f"empty_nav:{code}")

        items.append(
            {
                "code": code,
                "name": name,
                "nav": nav,
                "navBasis": nav_basis,
                "dwjz": dwjz,
                "gsz": gsz,
                "gztime": str(gz.get("gztime", "")),
                "source": "fundgz.1234567.com.cn",
            }
        )

    payload = {
        "asOf": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": "eastmoney_fundgz",
        "policy": "dwjz_first_then_gsz_fallback",
        "items": items,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    dwjz_used = sum(1 for i in items if i.get("navBasis") == "dwjz")
    gsz_used = sum(1 for i in items if i.get("navBasis") == "gsz_fallback")
    print(f"NAV_SNAPSHOT_OK items={len(items)} asOf={payload['asOf']} dwjz={dwjz_used} gsz_fallback={gsz_used}")


if __name__ == "__main__":
    main()
