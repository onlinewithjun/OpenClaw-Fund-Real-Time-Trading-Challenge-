[FUND_CHALLENGE_MODE]
Lightweight end-of-day review.
- Keep output concise and token-efficient.
- Use state.json + ledger.jsonl + status_brief.py result.
- Review checklist before concluding:
  - pending guard only blocks same-code conflict or insufficient cash, not unrelated redeem-in-flight
  - BUY candidates must remain Alipay-allowed
  - judge with Macro 30%, Sentiment 25%, Sector 25%, Quant 20%
  - flag low-quality rebuy / churn risk on names redeemed within the last 3 days
- Provide: (1) today summary, (2) what worked/failed, (3) next-day watchlist (max 3 items).
- If key data unverifiable, output DECISION_ABORTED_UNVERIFIED_DATA.
