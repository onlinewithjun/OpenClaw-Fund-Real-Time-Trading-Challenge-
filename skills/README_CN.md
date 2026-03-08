# Skills 目录说明

## 概述

本目录包含所有 OpenClaw 技能，按来源分为两类：

- **`original/`** - 原创开发的技能，受版权保护
- **`opensource/`** - 从 ClawHub 和社区下载的开源技能

## 目录结构

```
skills/
├── README.md              # 双语文档
├── README_CN.md           # 本文档（纯中文）
├── original/              # 原创版权技能
│   ├── fund-challenge-*/  # 1000 元基金挑战系列（12 个技能）
│   └── frontend-design/   # 前端 UI 设计生成器
└── opensource/            # 开源社区技能
    ├── alphaear-*/        # 金融分析系列（9 个技能）
    ├── arc-*/             # Agent 工作流系列（3 个技能）
    └── ...                # 其他社区技能（20+ 个技能）
```

---

## 原创技能 (original/)

### 基金实盘挑战系列

**版权所有** © 2026 lizhuojun. 保留所有权利.  
**作者**：lizhuojun  
**联系**：lzjouc@gmail.com

这是为"1000 元激进型基金实盘挑战"专门开发的完整工作流系统，包含 12 个协同工作的技能。

#### 核心技能说明

| # | 技能名称 | 功能描述 | 触发条件 |
|---|----------|----------|----------|
| 1 | **fund-challenge-orchestrator** | 主协调器，协调整个挑战工作流的执行顺序 | 挑战模式任务 |
| 2 | **fund-challenge-market-calendar-gate** | 验证是否为交易日、检查交易截止时间、市场时机约束 | 每次交易决策前 |
| 3 | **fund-challenge-identity-freshness-guard** | 验证基金代码与名称匹配、检查数据新鲜度、防止幻觉 | 基金推荐前 |
| 4 | **fund-challenge-signal-fusion-engine** | 融合政策/新闻信号、板块热度、宏观信号，生成排序机会 | 信号分析阶段 |
| 5 | **fund-challenge-position-risk-engine** | 计算仓位敞口、集中度风险、止损止盈点位 | 仓位管理阶段 |
| 6 | **fund-challenge-offexchange-exec-sim** | 模拟 T+ 确认/结算机制、申购/赎回限制、截止可行性 | 执行前模拟 |
| 7 | **fund-challenge-ledger-postmortem** | 状态持久化、账本审计、交易后审查与学习反馈 | 交易完成后 |
| 8 | **fund-challenge-daily-trader-core** | 端到端日常工作流，整合所有子技能 | 每日定时任务 |
| 9 | **fund-challenge-data-guard** | 数据完整性校验、防幻觉护栏、强制代码 - 名称匹配 | 数据获取后 |
| 10 | **fund-challenge-evidence-audit** | 证据捕获、引用完整性验证、决策门控（PLAN_ONLY→EXECUTE_READY） | 决策转换点 |
| 11 | **fund-challenge-execution-engine** | 短期激进操作的执行引擎和风险管理 | 执行阶段 |
| 12 | **fund-challenge-instrument-rules** | 解析每只基金的具体交易规则（申购/赎回限制、T+n 确认等） | 工具级规则查询 |

#### 工作流顺序

```
市场日历验证 → 身份/新鲜度验证 → 信号融合 → 仓位风险计算 → 执行模拟 → 账本记录
     ↓                                                                              ↓
  交易时间检查                                                              交易后审查/学习
```

#### 硬约束

- 必须首先读取 `fund_challenge/state.json` 状态文件
- 所有数值计算必须使用 `python fund_challenge/scripts/state_math.py --state fund_challenge/state.json`
- 如果任何关键数据无法验证：输出 `DECISION_ABORTED_UNVERIFIED_DATA`
- 仅在挑战模式下激活，普通投资建议请求不使用此技能栈

#### 使用示例

**触发关键词**：
- "基金实盘挑战"
- "1000 元挑战"
- cron 任务名 "基金实盘 - ..."

---

### 前端设计 (frontend-design)

**版本**：1.0.0  
**来源**：OpenClaw 官方

生成现代化、响应式的前端 UI 设计和组件。

#### 支持的框架

| 框架 | 版本 | 组件类型 | 样式方案 |
|------|------|----------|----------|
| React | 18+ | 函数组件、Hooks | Tailwind、MUI、CSS Modules |
| Vue | 3+ | 组合式 API | Tailwind、Element Plus |
| Angular | 15+ | 独立组件 | Angular Material、Tailwind |
| Svelte | 4+ | Svelte 组件 | Tailwind、原生 CSS |
| 纯 HTML/CSS | HTML5、CSS3 | 语义化 HTML | Tailwind、Bootstrap、自定义 |

#### 设计类别

- **布局组件**：导航栏、侧边栏、页脚、网格系统
- **表单组件**：输入框、下拉菜单、复选框、单选按钮
- **数据展示**：表格、卡片、列表、图表容器
- **反馈组件**：模态框、通知、加载状态、进度条
- **交互组件**：按钮组、标签页、手风琴、下拉菜单

#### 特性

- ✅ 响应式设计（移动优先、自适应布局）
- ✅ 无障碍访问（WCAG 2.1 合规、ARIA 属性）
- ✅ 性能优化（代码分割、懒加载）
- ✅ SEO 友好（语义化 HTML、meta 标签）

---

## 开源技能 (opensource/)

### AlphaEar 金融分析系列

AlphaEar 是一套完整的金融分析工具链，覆盖从数据获取到决策支持的全流程。

| 技能名称 | 核心功能 | 使用场景 |
|----------|----------|----------|
| **alphaear-news** | 从微博、知乎、华尔街见闻等 10+ 来源获取热门财经新闻，统一趋势分析 | 实时市场情绪监控 |
| **alphaear-stock** | 搜索 A 股/港股/美股股票代码，获取历史价格数据、技术指标 | 股票查询与基本面分析 |
| **alphaear-search** | 财经网络搜索（Jina/DDG/百度）+ 本地文档 RAG 检索 | 信息检索与知识查询 |
| **alphaear-sentiment** | 使用 FinBERT 或 LLM 分析财经文本情感（正面/负面/中性） | 新闻/报告情感分析 |
| **alphaear-predictor** | 基于 Kronos 模型的时间序列预测，支持新闻感知调整 | 市场走势预测 |
| **alphaear-reporter** | 生成专业财经报告、图表配置（Draw.io）、结构化输出 | 投研报告撰写 |
| **alphaear-signal-tracker** | 跟踪投资信号演变，判断信号增强/减弱/证伪 | 信号生命周期管理 |
| **alphaear-logic-visualizer** | 创建可视化财经逻辑图（Draw.io XML），解释复杂传导链 | 逻辑可视化展示 |
| **alphaear-deepear-lite** | 从 DeepEar Lite 仪表板获取最新财务信号和传导链分析 | 实时信号获取 |

#### 典型工作流

```
新闻获取 (alphaear-news)
    ↓
情感分析 (alphaear-sentiment)
    ↓
信号融合 (alphaear-signal-tracker)
    ↓
市场预测 (alphaear-predictor)
    ↓
报告生成 (alphaear-reporter)
    ↓
逻辑可视化 (alphaear-logic-visualizer)
```

---

### ARC Agent 工作流系列

ARC（Agent Runtime Control）系列提供 Agent 技能的管理、编排和安全审计能力。

| 技能名称 | 功能描述 | 使用场景 |
|----------|----------|----------|
| **arc-workflow-orchestrator** | 将多个技能链接成自动化管道，支持条件逻辑、错误处理、审计日志 | 复杂任务自动化 |
| **arc-skill-gitops** | GitOps 风格的技能生命周期管理：自动部署、回滚、版本控制 | 技能部署与运维 |
| **arc-security-audit** | 全面审计 Agent 技能栈的漏洞、权限问题、安全反模式 | 安全合规检查 |

---

### 工具与效率技能

#### 个人效率

| 技能名称 | 描述 | 特色功能 |
|----------|------|----------|
| **2nd-brain** | 个人知识库，用于捕获和检索人物、地点、餐厅、游戏、技术等信息 | AI 代理的第二大脑 |
| **agent-daily-planner** | 结构化每日计划与执行跟踪系统，包含晨间计划、任务跟踪、日终回顾 | 时间管理 |
| **alex-session-wrap-up** | 会话结束自动化：提交未推送工作、提取学习成果、检测模式、持久化规则 | 知识沉淀 |
| **active-maintenance** | 自动化系统健康检查和记忆代谢，清理资源、维护最优性能 | 系统维护 |
| **ai-daily-digest** | 从 90+ 个 AI/科技博客（Karpathy 精选）获取 RSS，AI 评分过滤，生成每日摘要 | 信息聚合 |

#### 开发与代码

| 技能名称 | 描述 | 支持语言 |
|----------|------|----------|
| **bat-cat** | cat 命令的增强克隆版，支持语法高亮、行号、Git 集成 | 所有文本文件 |
| **code-review** | 系统化代码审查模式，覆盖安全性、性能、可维护性、正确性、测试 | 全语言支持 |
| **code-simplifier** | 简化和重构代码，降低复杂度、提高可读性、保持功能 | C++/Python/JS/TS/Java |
| **pr-review** | 自动化 Pull Request 审查，集成 GitHub，管理标签，CI/CD 集成 | GitHub 项目 |
| **security-auditor** | 代码库全面安全审计，检测漏洞、安全反模式、合规问题（OWASP/CWE/SANS） | 多语言支持 |
| **skill-creator** | 创建或更新 AgentSkills，支持脚本、参考文档、资源打包 | OpenClaw 技能开发 |
| **test-case-generator** | 测试用例生成工具 | 多语言支持 |

#### 金融与投资

| 技能名称 | 描述 | 支持市场 |
|----------|------|----------|
| **akshare-skill** | 使用 AkShare 库访问中国金融数据：A 股、港股、美股、期货、基金、宏观指标 | 中国金融市场 |
| **etf-assistant** | ETF 投资助理：查询行情、筛选 ETF、对比分析、定投计算 | 沪深 300、创业板、科创 50、纳指等 |
| **charts** | 图表生成和可视化工具 | 通用 |

#### 研究与内容

| 技能名称 | 描述 | 特色 |
|----------|------|------|
| **research-cog** | 由 CellCog 驱动的深度研究 Agent，支持市场调研、竞争分析、股票分析、学术研究 | DeepResearch Bench 2026 年 2 月第 1 名 |
| **summarize** | 总结 URL 或文件内容（网页、PDF、图片、音频、YouTube） | 多格式支持 |
| **apipick-company-facts** | 公司事实和商业智能查询 | 企业信息 |
| **xiaohongshu-mcp** | 小红书 MCP 集成，支持内容发布、数据分析 | 小红书平台 |

---

## 技能使用指南

### 如何选择合适的技能

1. **基金实盘挑战任务** → 使用 `fund-challenge-*` 系列（仅限挑战模式）
2. **普通投资建议** → 使用 `alphaear-*` 系列或 `etf-assistant`
3. **代码开发** → 使用 `code-review`、`code-simplifier`、`security-auditor`
4. **市场研究** → 使用 `research-cog`、`alphaear-news`、`alphaear-search`
5. **日常工作流** → 使用 `agent-daily-planner`、`active-maintenance`

### 技能组合示例

#### 示例 1：基金投资决策
```
alphaear-news (获取新闻)
  → alphaear-sentiment (情感分析)
  → alphaear-stock (查询股票代码)
  → etf-assistant (ETF 对比分析)
  → 输出投资建议
```

#### 示例 2：代码审查工作流
```
code-review (初步审查)
  → security-auditor (安全审计)
  → code-simplifier (简化重构)
  → pr-review (创建 PR 审查)
```

#### 示例 3：深度研究报告
```
research-cog (深度研究)
  → alphaear-reporter (生成报告)
  → alphaear-logic-visualizer (可视化逻辑图)
```

---

## 许可证

### 原创技能
`original/` 目录中的所有技能：
- **版权所有** © 2026 lizhuojun. 保留所有权利。
- **作者**：lizhuojun
- **联系**：lzjouc@gmail.com
- **许可**：未经许可，不得用于商业用途

### 开源技能
`opensource/` 目录中的技能遵循各自的开源许可证：
- 大部分技能使用 MIT、Apache 2.0 或 ISC 许可证
- 具体许可证请查看各技能目录中的 `LICENSE` 文件或 `SKILL.md` 头部

---

## 更新日志

### 2026-03-08
- ✅ 完成 skills 目录重组，分为 `original/` 和 `opensource/`
- ✅ 添加 13 个原创技能（12 个基金挑战系列 + frontend-design）
- ✅ 整理 32 个开源技能
- ✅ 创建双语文档（README.md 和 README_CN.md）

### 2026-03-04 ~ 2026-03-07
- 开发基金实盘挑战系列技能（12 个）
- 实现完整的挑战工作流和风险控制机制

### 2026-02-27 ~ 2026-03-01
- 从 ClawHub 下载并整合开源技能
- 配置 Telegram bot 和 qmd 搜索系统

---

## 联系方式

- **作者**：lizhuojun
- **邮箱**：lzjouc@gmail.com
- **GitHub**：https://github.com/onlinewithjun
- **项目**：OpenClaw Fund Real-Time Trading Challenge
