# OpenClaw 基金实盘挑战分支

这是一个面向**1000 元场外基金短线激进挑战**的专用分支，强调稳定执行、可追溯、低 token 开销。

## 目标

- 初始资金：**1000 元**
- 目标：**6 个月翻倍**
- 平台：**支付宝 / 天天基金**
- 风格：**短线激进**（但必须通过证据与风控门）

---

## 分支范围

本分支只保留挑战相关内容：

- `fund_challenge/`：挑战运行文件、状态、脚本、提示词
- `skills/fund-challenge-*`：挑战专用技能
- 必要的说明文档

不包含与本挑战无关的工程代码。

---

## 设计原则

1. **状态优先**：状态更新必须可追溯、可复核
2. **证据门控**：未通过证据校验，不允许进入 EXECUTE_READY
3. **执行可行性**：严格执行 T+、截止时间、申赎可行性规则
4. **低 token**：压缩输出、压缩证据、短格式发布
5. **单方案策略**：默认每次只给一个可执行方案

---

## 每日流程（交易日）

- **09:00** 健康检查（正常静默，异常短告警）
- **14:00** PLAN_ONLY
- **14:48** EXECUTE_READY 最终门控（单方案）
- **20:05** 日终更新
- **20:25** 轻量复盘
- **21:00** 维护任务（缓存清理）

---

## 你需要做的事

你只需要在收到 BUY 指令后手动下单，并回复确认：

- `我已买入 020899 100元，14:52`
- `未执行：限购/暂停申购`

状态回写与流水记录由脚本自动处理。

---

## 文件说明（按目录）

## 1）`fund_challenge/` 根目录

- `state.json`
  - 当前持仓与资金的权威状态快照。
  - 仅在你明确确认执行后更新。

- `ledger.jsonl`
  - 事件流水（只追加，不回写历史）。

- `instrument_rules.json`
  - 生效中的基金/平台执行约束（T+、截止、状态等）。

- `instrument_rule_sources.json`
  - 规则来源映射（优先来源与备用来源）。

- `receipt.template.json`
  - 执行确认回执模板。

- `decision_history.jsonl`（运行时生成）
  - 同日重复决策去重记录。

---

## 2）`fund_challenge/prompts/`

- `0900-healthcheck.md`：健康检查说明
- `1400-open.md`：14:00 预案说明
- `1420-track.md`：盘中跟踪（轻量）
- `1440-decision.md`：尾盘最终门控说明
- `2000-update.md`：收盘更新说明
- `2025-review.md`：轻量复盘说明

---

## 3）`fund_challenge/evidence/`

- `template.json`：证据模板
- `latest.json`（运行时）：最新证据
- `latest.compact.json`（运行时）：压缩证据（省 token）
- `README.md`：证据字段规范

---

## 4）`fund_challenge/scripts/`（按功能）

### 管线与调度
- `run_decision_pipeline.py`：端到端低 token 决策流水线
- `daily_bundle_runner.py`：预检+状态简报的一键轻量流程
- `preflight_guard.py`：预检总闸（支持 compact）

### 状态与计算
- `state_math.py`：资金/盈亏确定性计算
- `execution_receipt_updater.py`：按确认回执更新 state+ledger
- `confirm_and_apply.py`：文本确认到回写的一键流程

### 证据与发布门控
- `build_evidence.py`：生成证据文件
- `validate_evidence.py`：证据字段与阶段校验
- `decision_publish_gate.py`：无充分证据禁止发布执行指令
- `evidence_compactor.py`：证据瘦身
- `decision_packet_builder.py`：打包发布用决策包

### 执行确认解析
- `receipt_from_text.py`：把自然语言确认转成回执 JSON
- `decision_id_linker.py`：回执绑定 decisionId

### 低 token / 高效率工具
- `source_fetch_minifier.py`：长文本来源压缩
- `runtime_cache.py`：TTL 运行缓存
- `cache_key_builder.py`：稳定缓存键
- `status_brief.py`：超短状态行
- `decision_template_shortener.py`：决策文案短格式化
- `decision_delta_guard.py`：同日重复决策防抖
- `fast_fail_report.py`：失败短告警（默认 HOLD）
- `refresh_instrument_rules.py`：规则元数据刷新

---

## 5）`skills/fund-challenge-*`

这些技能按职责拆分（编排、校验、执行、规则、复盘），仅用于基金挑战场景，不用于普通理财咨询。

---

## Cron 运行策略

当前采用“拆分小任务”以降低超时和阻塞：

- 09:00 健康检查
- 14:00 预案
- 14:48 最终门控
- 20:05 更新
- 20:25 复盘
- 21:00 维护

建议参数：isolated、low/minimal thinking、exact、light-context、best-effort-deliver。

---

## 安全底线

只要关键数据/来源不可验证，必须输出：

`DECISION_ABORTED_UNVERIFIED_DATA`

并降级为 **HOLD**。
