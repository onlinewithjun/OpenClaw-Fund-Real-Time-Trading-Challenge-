# 2026-04-03 更新日志

> 本次更新共计 42 个 commit，重点修复了 Telegram 投递链路、Bug 4 冷却guard、Bug 3 信号背离标注、Bug 5 达标de-risk 提醒，并对候选池质量、并发控制和风控逻辑做了系统性加固。

---

## 一、核心 Bug 修复

### 🐛 P0｜Bug 1：Telegram announcement 投递链路中断
**问题**：所有非盘中时段的 isolated session cron（晚间 21:xx、早间 09:xx、凌晨 01~03xx、周报等）全部报错 `Outbound not configured for channel: telegram`，但盘中 14:xx cron 正常。连续失败 2 次。  
**根因**：isolated session 在非交易时段 announcement 投递路由失败。  
**修复**：16 个失败的 cron jobs 全部从 `sessionTarget=isolated` 改为 `sessionTarget=current`，绑定主 session 确保 announcement 投递上下文正确。

| 受影响任务 | 修复前 | 修复后 |
|-----------|--------|--------|
| 基金挑战 #09~#16（晚间批次） | isolated | current |
| 基金挑战 #17（凌晨策略复查） | isolated | current |
| 晨报 US close、AI 24h、港股/A股晚报 | isolated | current |
| workspace-secret-scan、memory维护 | isolated | current |

---

### 🐛 P2｜Bug 4：execute gate 加"5天内同类操作>=2"冷却拦截
**问题**：MEMORY.md 铁律明确禁止"昨天卖、今天买回"低质量打脸循环，但 execute gate 层面无此保护，曾导致 4/1~4/2 连续逆向操作。  
**修复**：
- 新增 `recent_action_map()`：追踪每个基金代码 5 天内 REDEEM 和 BUY 次数
- 新增 `cooldown_violation()`：同一代码、同一操作类型、5天内出现>=2次 → 拦截并返回冷却违规原因
- 在 execute gate 的 3 个决策分支（REDEEM_REDUCE / TRIAL_BUY / raise_cash）中全部集成

**触发效果示例**：
```
cooldown_redeem_violation_002611_within_5d_count=2  →  HOLD
cooldown_buy_violation_000056_within_5d_count=2     →  HOLD
```

---

### 🐛 P2｜Bug 3：plan 输出加信号背离标注
**问题**：000056 建信消费升级今日以 78 元建仓，但量化信号 rank=#10（倒数第二），与量化系统脱节。  
**修复**：`generate_full_plan_report()` 对每个持仓标注 quant rank，当 rank >= 8 时追加 `[Signal Deviation Alerts]` 段落：
```
ALERT: 000056 is ranked #10 (quant signal weak) but still held - review for reduction or exit
```

---

### 🐛 P2｜Bug 5：PV 达标时主动推 de-risk 提醒
**问题**：3/31 组合净值冲高到 2004（distanceToTarget=-4.41），系统无任何提示。  
**修复**：`generate_full_plan_report()` 检测到 `portfolioValue >= target` 时追加：
```
** DE-RISK RECOMMENDED: Strongly consider REDEEMING profits rather than initiating new BUYs **
```

---

## 二、候选池质量加固

### 🔧 候选池刷新逻辑强化
**改动**：
- 强制保留现有持仓基金，即使其不在当日候选列表中
- 过滤支付宝不可买的基金（定开封闭、QDII 等）
- 扩展候选池上限至 50 只（tech:18, cyclical:12, gold:8, index:12）
- 新增 `alipay_allowed.json`：支付宝可买基金白名单，仅白名单内基金可参与排序和执行
- 增强同系份额去重：合并 A/C/I/H/E 类份额，优先保留持仓中已有份额

---

## 三、风控与执行纪律

### 🛡️ Pending 交易 SLA 纪律
- Pending BUY 超过 1 个交易日 → 标记为 stale，触发告警
- Pending REDEEM 为 informational，不自动拦截不同代码的 BUY
- 新增 `auto_close_stale_pending.py`：自动关闭超时期权性 pending
- Pending 冲突时只 block 同代码、不同代码 + 现金充足 = 允许

### 📊 集中度控制
- 单只基金市值占比 >= 30% → 拒绝加仓
- 单一行业占比 >= 45% → 拒绝加仓

### 📈 Drawdown  tier sizing
| Drawdown | 最大买入占比 |
|---------|------------|
| <= -5% | 10% PV |
| <= -3% | 8% PV |
| <= -1% | 5% PV |
| > -1% | 5% PV（floor） |
| 组合触及 2000 目标 | buy_pct=0（硬止） |

---

## 四、模型与服务配置

### ⚙️ 模型迁移
- 默认模型从 bailian 迁移至 minimax m2.7
- 决策框架：Macro 30% / Sentiment 25% / Sector 25% / Quant 20%
- Quant 数据仅作参考，不主导决策

### 📡 Cron 任务清理与规范化
- 14:xx 盘中批次正常（#03~#08，delivery=delivered）
- 非盘中批次修复后统一为 `sessionTarget=current`
- 01:20 策略复查增设审查清单（pending order 检查、基金推荐铁律验证等）

---

## 五、其他

- 新增一次性修复脚本：`add_017192_redeem.py`、`fix_pending_020899.py`、`fix_state_manual.py`
- Memory 归档：超过 7 天的日记录移至 `memory/archive/`
- `MEMORY.md` 保持精简，仅保留长期稳定信息

---

## 六、未解决问题（需关注）

### ⚠️ Bug 2：4/1~4/2 逆向操作根因待查
从 ledger MTM 记录看：
```
03-31 21:00  PV=2004（达标）
04-01 21:00  PV=891（清仓式卖出，pendingRedeem=180元）
04-02 21:00  PV=986（快速买回）
```
缺乏逻辑连贯性，可能是 auto_close_stale_pending 和人工操作打架。建议在下次 #17 凌晨策略复查（01:20）中专项审计这两天操作链，确认机制面有无漏洞。

---

*Generated at 2026-04-03 17:38 CST · 共 42 commits · branch: fund-challenge-only*
