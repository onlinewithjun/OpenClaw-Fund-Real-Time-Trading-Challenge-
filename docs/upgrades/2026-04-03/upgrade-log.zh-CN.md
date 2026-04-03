# 升级日志（2026-04-03）

## 一、Telegram Announcement 投递链路修复（P0）

**问题**：所有非盘中时段的 isolated session cron（晚间 21:xx、早间 09:xx、凌晨 01~03xx、周报等）全部报错 `Outbound not configured for channel: telegram`，连续失败 2 次；但盘中 14:xx cron 完全正常。

**根因**：isolated session 在非交易时段 announcement 投递路由失败，与 `sessionKey` 配置无关。

**修复**：16 个失败的 cron jobs 全部从 `sessionTarget=isolated` 改为 `sessionTarget=current`，绑定主 session 确保 announcement 投递上下文正确。

受影响的 cron 任务：
- 基金挑战 #09~#16（晚间更新/重试/复盘/运维批次）
- 基金挑战 #17（凌晨 01:20 策略复查）
- workspace-secret-scan-daily、memory-maintenance-daily
- 晨报（US close、AI 24h、港股晚报、A 股晚报）

---

## 二、执行层冷却 Guard（P2 - Bug 4）

**问题**：MEMORY.md 铁律明确禁止"昨天卖、今天买回"低质量打脸循环，但 execute gate 层面此前无此保护，曾导致 4/1~4/2 连续逆向操作（002611 连续卖出后快速买回 000056）。

**修复**：
- 新增 `recent_action_map()`：追踪每个基金代码 5 天内 REDEEM 和 BUY 次数（从 ledger.jsonl 读取）
- 新增 `cooldown_violation()`：同一代码、同一操作类型、5 天内出现 >=2 次 → 拦截并返回冷却违规原因
- 在 `execute_gate_script_only.py` 的 3 个决策分支（REDEEM_REDUCE / TRIAL_BUY / raise_cash）中全部集成

触发效果示例：
```
cooldown_redeem_violation_002611_within_5d_count=2  →  HOLD
cooldown_buy_violation_000056_within_5d_count=2     →  HOLD
```

---

## 三、Plan 报告信号背离标注（P2 - Bug 3）

**问题**：000056 建信消费升级混合当日以 78 元人工建仓，但量化信号 rank=#10（倒数第二），score=61.4，confidence=0.72，与量化系统严重脱节，无任何提示。

**修复**：`generate_full_plan_report()` 对每个持仓标注 quant rank，当 rank >= 8 时追加 `[Signal Deviation Alerts]` 段落：
```
ALERT: 000056 is ranked #10 (quant signal weak) but still held - review for reduction or exit
```

---

## 四、PV 达标 De-risk 提醒（P2 - Bug 5）

**问题**：3/31 组合净值冲高到 2004（distanceToTarget=-4.41），系统无任何提示，用户未及时获知。

**修复**：`generate_full_plan_report()` 检测到 `portfolioValue >= target` 时，在 `[Portfolio]` 段落下方追加：
```
** DE-RISK RECOMMENDED: Strongly consider REDEEMING profits rather than initiating new BUYs **
```

---

## 五、待专项审计问题（Bugs 待查）

### ⚠️ 4/1~4/2 逆向操作根因待查

从 ledger MTM 记录观察：
```
03-31 21:00  PV=2004（达标）
04-01 21:00  PV=891（清仓式卖出，pendingRedeem=180元）
04-02 21:00  PV=986（快速买回）
```

缺乏逻辑连贯性，可能是 `auto_close_stale_pending` 和人工操作打架。建议在下次 #17 凌晨策略复查（01:20）中专项审计这两天操作链。

---

## 六、其他变更

- 新增一次性修复脚本：`add_017172_redeem.py`、`fix_pending_020899.py`、`fix_state_manual.py`
- Memory 日归档：超过 7 天的日记录移至 `memory/archive/`
- `MEMORY.md` 保持精简，仅保留长期稳定信息
