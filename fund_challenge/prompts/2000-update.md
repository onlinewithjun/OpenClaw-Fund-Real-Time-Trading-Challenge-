[FUND_CHALLENGE_MODE]
Post-close update only.
- Recompute state using script
- Do not alter holdings unless user confirmed execution
- If user confirmed, prefer confirm_and_apply.py with --link-decision-id
- Emit compact status line via status_brief.py for end-of-day message
- Append ledger event
- Summarize PnL, drawdown, and next-day watchlist
