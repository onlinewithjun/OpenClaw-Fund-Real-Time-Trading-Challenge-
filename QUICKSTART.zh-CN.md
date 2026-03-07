# QUICKSTART（3分钟）

## 1）启动前检查（一次即可）

```bash
python fund_challenge/scripts/state_math.py --state fund_challenge/state.json
openclaw cron list --all
```

## 2）交易日的最小操作

- 14:00：收到 PLAN_ONLY 预案
- 14:48：收到 EXECUTE_READY（只给一个可执行方案）
- 若指令为 BUY：你在支付宝/天天基金手动下单（15:00前）
- 下单后回复确认，例如：
  - `我已买入 020899 100元，14:52`
  - `未执行：限购`

## 3）一键确认并回写

```bash
python fund_challenge/scripts/confirm_and_apply.py --text "我已买入 020899 100元" --link-decision-id
```

## 4）应急规则

- 关键数据不可验证：`DECISION_ABORTED_UNVERIFIED_DATA` + HOLD
- 计划不可执行（限购/暂停/超时）：当下 HOLD，随后给下一可执行单方案
- 你未确认执行：不更新 state/ledger

## 5）常用诊断命令

```bash
python fund_challenge/scripts/status_brief.py
python fund_challenge/scripts/daily_bundle_runner.py --phase PLAN_ONLY
openclaw cron runs --limit 20
```
