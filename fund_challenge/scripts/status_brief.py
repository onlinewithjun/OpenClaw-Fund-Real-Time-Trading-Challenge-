from __future__ import annotations

import argparse
import json
from pathlib import Path

from state_math import compute


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate compact challenge status line")
    ap.add_argument("--state", default="fund_challenge/state.json")
    ap.add_argument("--max-holdings", type=int, default=3)
    args = ap.parse_args()

    state = load_json(Path(args.state))
    digest = compute(state)
    holdings = state.get("holdings", [])[: args.max_holdings]

    parts = [
        f"PV {digest['portfolioValue']}",
        f"UPnL {digest['totalUnrealizedPnl']}",
        f"Gap {digest['distanceToTarget']}",
    ]

    for h in holdings:
        code = h.get("code", "?")
        pnl = h.get("unrealizedPnl", "?")
        parts.append(f"{code}:{pnl}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
