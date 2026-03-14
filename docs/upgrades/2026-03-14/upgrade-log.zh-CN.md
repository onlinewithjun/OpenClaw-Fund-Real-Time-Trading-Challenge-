# 升级日志（2026-03-14）

## 一、模型与网关
- 放行并启用默认主模型 `openai-codex/gpt-5.4`。
- 修复 OpenClaw gateway service 路径漂移问题，使服务入口与当前 nvm 安装路径一致。
- 清理 session store：删除 transcript 缺失的脏索引与 orphan transcript 文件，`openclaw doctor` 不再报告对应问题。

## 二、Memory 与上下文优化
- 压缩 `MEMORY.md`，仅保留长期稳定信息。
- 新增 `memory/2026-03-14.md` 记录当天维护与策略演进。
- 归档旧 daily memory 到 `memory/archive/`，并归档短期专项报告到 `memory/archive/special/`。
- 在 `AGENTS.md` 中加入“上下文高水位自动写 memory”规则。
- 新增每日 `Memory maintenance` 定时任务，用于自动审视、归档和压缩 memory。
- 记录用户偏好：允许在不影响体验前提下主动做低风险优化，不必逐项询问。

## 三、基金挑战系统修复
- 补上 `update_refresh_retry.py` 的晚间自动重试调度：新增 #06b~#06f 更新重试任务。
- 升级 `healthcheck_brief.py`：
  - 不再只检查文件与语法；
  - 增加 `state.json`、`daily_candidates.json`、`consistency_04b.json` 的关键时间窗新鲜度校验；
  - 新增非交易日友好模式，周末/非交易日返回 `HEALTHCHECK_OK NON_TRADING_DAY ...`。
- 新增 `fund_challenge/scripts/maintenance_cleanup.py`：
  - runtime cache prune
  - 清理 `out/` 临时失败文件
  - 归档旧 evidence
  - 清理 `__pycache__`
  - 清理过旧 runtime snapshots
  - 清理历史嵌套残留目录
- 将 #08 维护任务切换到 `maintenance_cleanup.py`。
- 将 `execute_gate_script_only.py` 中的 `TARGET_REMAP` 硬编码迁移至 `instrument_rules.json.targetRemap`。

## 四、基金挑战策略升级
- 从“短线框架但偏保守”升级为更接近“短线激进但不盲目追涨”的策略逻辑。
- 升级 `gate_scoring.py`：
  - 新增强势切换识别
  - 增加 `strongSwitchCount` / `pullbackCount`
  - 引入 `confidenceTier`（A/B/C）
  - 引入 `suggestedBuyPct`
  - 优化 momentum scoring 与 risk switch 判定
- 升级 `execute_gate_script_only.py`：
  - 新增双通道买入：回撤低吸 + 强势切换
  - 买入仓位不再固定 5%，改为读取 evidence 给出的建议仓位
  - 卖出目标从“最差盈亏排序”升级为“预期失败优先卖”
- 保留 stale/freshness guard 与真实外部执行确认边界，不让激进策略破坏基础风控。

## 五、基金挑战自治化
- 新增 `基金挑战#09-01:20策略复盘优化` isolated cron：
  - 每日凌晨自动复盘
  - 自动学习与微调 challenge 内部策略/维护逻辑
  - 写入 memory 并提交相关变更
- 记录用户授权：基金挑战策略层完全放权，允许 AI 主动推进策略、复盘、优化和调度；真实外部买卖仍保留最终执行/确认边界。
