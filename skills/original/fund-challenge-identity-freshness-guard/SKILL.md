---
name: fund-challenge-identity-freshness-guard
description: Strict fund code-name verification and data freshness guard for challenge mode. Use only in challenge tasks to prevent wrong fund mapping, stale evidence, and fabricated inputs.
---

# Fund Challenge Identity Freshness Guard

Copyright (c) 2026 lizhuojun. All rights reserved.  
Author: lizhuojun  
Email: lzjouc@gmail.com

## Mandatory identity verification

For each fund candidate and holding:

- Query: `"<code> <fund_name> 天天基金网"`
- Query: `"<fund_name> 基金代码 天天基金"`
- Require exact code-name match; otherwise mark `INVALID_FOR_TRADE`.

## Mandatory freshness verification

- Attach timestamp for each market input.
- Reject stale inputs for short-term rotation decisions.

## Citation policy

Include evidence lines in decision artifacts:

- `Source: <url/site> @ <timestamp>`

## Abort policy

Return `DECISION_ABORTED_UNVERIFIED_DATA` when identity or freshness checks fail.
