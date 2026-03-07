from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEF_TZ = "+08:00"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_rules(rules: dict, src_map: dict) -> dict:
    out = dict(rules)
    out.setdefault("metadata", {})
    out["metadata"]["lastRefreshedAt"] = now_iso()
    out["metadata"]["sourceMappingVersion"] = src_map.get("version", "unknown")

    funds = out.setdefault("funds", {})
    fund_src = src_map.get("fundSourceMap", {})

    for code, fm in funds.items():
        source_def = fund_src.get(code, {})
        fm.setdefault("verification", {})
        fm["verification"]["sourcePlatform"] = "TiantianFund"
        fm["verification"]["sourceUrl"] = (source_def.get("preferredSources") or [None])[0]
        fm["verification"]["fallbackSources"] = source_def.get("fallbackSources", [])
        fm["verification"]["lastNoticeAt"] = None
        fm["verification"]["refreshState"] = "needs_live_fetch"

    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Refresh instrument rules metadata and source mapping")
    ap.add_argument("--rules", required=True, help="Path to instrument_rules.json")
    ap.add_argument("--sources", required=True, help="Path to instrument_rule_sources.json")
    args = ap.parse_args()

    rules_path = Path(args.rules)
    src_path = Path(args.sources)

    rules = load_json(rules_path)
    src_map = load_json(src_path)
    merged = merge_rules(rules, src_map)
    save_json(rules_path, merged)

    print(json.dumps({
        "status": "ok",
        "rules": str(rules_path),
        "sources": str(src_path),
        "refreshedAt": merged.get("metadata", {}).get("lastRefreshedAt"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
