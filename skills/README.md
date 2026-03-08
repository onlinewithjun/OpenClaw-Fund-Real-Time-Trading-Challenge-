# Skills Directory / Skills 目录

[English](#english) | [中文](#中文)

---

## English

### Overview

This directory contains all OpenClaw skills organized into two categories:

- **`original/`** - Original skills developed in-house with copyright protection
- **`opensource/`** - Open-source skills downloaded from ClawHub and community contributions

### Directory Structure

```
skills/
├── README.md              # This file (bilingual documentation)
├── README_CN.md           # Chinese version only
├── original/              # Original copyrighted skills (12 total)
│   └── fund-challenge-*/  # 1000 CNY Fund Challenge series (12 skills)
└── opensource/            # Open-source community skills (33 total)
    ├── alphaear-*/        # Financial analysis series (9 skills)
    ├── arc-*/             # Agent workflow series (3 skills)
    ├── frontend-design/   # Frontend UI design generator
    └── ...                # Other community skills (21 skills)
```

---

### Original Skills (original/)

#### Fund Challenge Series (基金实盘挑战系列)

Copyright © 2026 lizhuojun. All rights reserved.

A complete workflow system for the 1000 CNY aggressive fund trading challenge.

| Skill Name | Description |
|------------|-------------|
| **fund-challenge-orchestrator** | Master orchestrator that coordinates the entire challenge workflow |
| **fund-challenge-market-calendar-gate** | Validates trading days, cutoff times, and market timing constraints |
| **fund-challenge-identity-freshness-guard** | Verifies fund code-name matching and data freshness |
| **fund-challenge-signal-fusion-engine** | Combines policy/news, sector heat, and macro signals into ranked opportunities |
| **fund-challenge-position-risk-engine** | Computes exposure, concentration, stop-loss, and take-profit actions |
| **fund-challenge-offexchange-exec-sim** | Simulates T+ confirmation/settlement and subscription/redemption limits |
| **fund-challenge-ledger-postmortem** | State persistence, ledger audit, and post-trade review |
| **fund-challenge-daily-trader-core** | End-to-end daily workflow for aggressive off-exchange fund operations |
| **fund-challenge-data-guard** | Data integrity and anti-hallucination guardrail |
| **fund-challenge-evidence-audit** | Evidence capture and machine-auditable decision gating |
| **fund-challenge-execution-engine** | Execution and risk engine for short-term aggressive operations |
| **fund-challenge-instrument-rules** | Instrument-level trading rule resolver |

**Usage**: These skills activate ONLY when context explicitly indicates challenge mode ("基金实盘挑战", "1000 元挑战", or cron jobs named "基金实盘 - ...").

**Total**: 12 original skills (all fund-challenge series)

---

### Open-Source Skills (opensource/)

#### AlphaEar Financial Analysis Series

| Skill Name | Description |
|------------|-------------|
| **alphaear-news** | Fetch hot finance news and unified trends from multiple sources |
| **alphaear-stock** | Search A-Share/HK/US stock tickers and retrieve price history |
| **alphaear-search** | Perform finance web searches and local context searches |
| **alphaear-sentiment** | Analyze finance text sentiment using FinBERT or LLM |
| **alphaear-predictor** | Market prediction using Kronos time-series forecasting |
| **alphaear-reporter** | Generate professional financial reports and chart configurations |
| **alphaear-signal-tracker** | Track investment signal evolution and update logic |
| **alphaear-logic-visualizer** | Create visual finance logic diagrams (Draw.io XML) |
| **alphaear-deepear-lite** | Fetch latest financial signals from DeepEar Lite dashboard |

#### ARC Agent Workflow Series

| Skill Name | Description |
|------------|-------------|
| **arc-workflow-orchestrator** | Chain skills into automated pipelines with conditional logic |
| **arc-skill-gitops** | Automated deployment, rollback, and version management for skills |
| **arc-security-audit** | Comprehensive security audit for agent skill stacks |

#### Utility & Productivity Skills

| Skill Name | Description |
|------------|-------------|
| **2nd-brain** | Personal knowledge base for capturing and retrieving information |
| **active-maintenance** | Automated system health and memory metabolism |
| **agent-audit** | Audit AI agent setup for performance, cost, and ROI |
| **agent-daily-planner** | Structured daily planning and execution tracking |
| **ai-daily-digest** | Fetch RSS feeds from 90+ AI/tech blogs, generate daily summaries |
| **akshare-skill** | Chinese financial data access using AkShare library |
| **alex-session-wrap-up** | End-of-session automation with knowledge capture |
| **apipick-company-facts** | Company facts and business intelligence |
| **bat-cat** | Enhanced cat clone with syntax highlighting and Git integration |
| **charts** | Chart generation and visualization |
| **code-review** | Systematic code review patterns |
| **code-simplifier** | Simplify and refactor code to reduce complexity |
| **etf-assistant** | ETF investment assistant (沪深 300, 创业板，科创 50, 纳指等) |
| **frontend-design** | Generate modern, responsive frontend UI designs and components (React, Vue, Angular, Tailwind CSS, MUI) |
| **pr-review** | Automated Pull Request review with GitHub integration |
| **research-cog** | Deep research agent powered by CellCog (#1 on DeepResearch Bench) |
| **security-auditor** | Comprehensive security auditing for codebases |
| **skill-creator** | Create or update AgentSkills |
| **summarize** | Summarize URLs or files (web, PDFs, images, audio, YouTube) |
| **test-case-generator** | Test case generation utilities |
| **xiaohongshu-mcp** | Xiaohongshu (Little Red Book) MCP integration |

---

## 中文

### 概述

本目录包含所有 OpenClaw skills，分为两类：

- **`original/`** - 原创开发的技能，受版权保护
- **`opensource/`** - 从 ClawHub 和社区下载的开源技能

### 目录结构

```
skills/
├── README.md              # 本文件（双语文档）
├── README_CN.md           # 纯中文版本
├── original/              # 原创版权技能
│   ├── fund-challenge-*/  # 1000 元基金挑战系列（12 个技能）
│   └── frontend-design/   # 前端 UI 设计生成器
└── opensource/            # 开源社区技能
    ├── alphaear-*/        # 金融分析系列（9 个技能）
    ├── arc-*/             # Agent 工作流系列（3 个技能）
    └── ...                # 其他社区技能（20+ 个技能）
```

---

### 原创技能 (original/)

#### 基金实盘挑战系列

版权所有 © 2026 lizhuojun. 保留所有权利.

完整的 1000 元激进型基金实盘挑战工作流系统。

| 技能名称 | 描述 |
|----------|------|
| **fund-challenge-orchestrator** | 主协调器，协调整个挑战工作流 |
| **fund-challenge-market-calendar-gate** | 验证交易日、截止时间和市场时机约束 |
| **fund-challenge-identity-freshness-guard** | 验证基金代码 - 名称匹配和数据新鲜度 |
| **fund-challenge-signal-fusion-engine** | 将政策/新闻、板块热度和宏观信号融合为排序机会 |
| **fund-challenge-position-risk-engine** | 计算敞口、集中度、止损和止盈操作 |
| **fund-challenge-offexchange-exec-sim** | 模拟 T+ 确认/结算和申购/赎回限制 |
| **fund-challenge-ledger-postmortem** | 状态持久化、账本审计和交易后审查 |
| **fund-challenge-daily-trader-core** | 场外基金激进操作的端到端日常工作流 |
| **fund-challenge-data-guard** | 数据完整性和防幻觉护栏 |
| **fund-challenge-evidence-audit** | 证据捕获和机器可审计的决策门控 |
| **fund-challenge-execution-engine** | 短期激进操作的执行和风险引擎 |
| **fund-challenge-instrument-rules** | 工具级交易规则解析器 |

**使用说明**：仅当上下文明确指示挑战模式（"基金实盘挑战"、"1000 元挑战"或名为"基金实盘 - ..."的 cron 任务）时，这些技能才会激活。

#### 前端设计 (frontend-design)

生成现代化、响应式的前端 UI 设计和组件。

- **框架支持**：React、Vue、Angular、Svelte、纯 HTML/CSS/JS
- **样式库**：Tailwind CSS、Material UI、Ant Design、styled-components
- **特性**：响应式设计、无障碍访问（WCAG 2.1）、性能优化

---

### 开源技能 (opensource/)

#### AlphaEar 金融分析系列

| 技能名称 | 描述 |
|----------|------|
| **alphaear-news** | 从多个来源获取热门财经新闻和统一趋势 |
| **alphaear-stock** | 搜索 A 股/港股/美股股票代码并获取价格历史 |
| **alphaear-search** | 执行财经网络搜索和本地上下文搜索 |
| **alphaear-sentiment** | 使用 FinBERT 或 LLM 分析财经文本情感 |
| **alphaear-predictor** | 使用 Kronos 时间序列预测进行市场预测 |
| **alphaear-reporter** | 生成专业财经报告和图表配置 |
| **alphaear-signal-tracker** | 跟踪投资信号演变并更新逻辑 |
| **alphaear-logic-visualizer** | 创建可视化财经逻辑图（Draw.io XML） |
| **alphaear-deepear-lite** | 从 DeepEar Lite 仪表板获取最新财务信号 |

#### ARC Agent 工作流系列

| 技能名称 | 描述 |
|----------|------|
| **arc-workflow-orchestrator** | 将技能链接成带有条件逻辑的自动化管道 |
| **arc-skill-gitops** | 技能的自动化部署、回滚和版本管理 |
| **arc-security-audit** | 对 Agent 技能栈进行全面安全审计 |

#### 工具与效率技能

| 技能名称 | 描述 |
|----------|------|
| **2nd-brain** | 用于捕获和检索信息的个人知识库 |
| **active-maintenance** | 自动化系统健康和记忆代谢 |
| **agent-audit** | 审计 AI Agent 设置的性能、成本和 ROI |
| **agent-daily-planner** | 结构化每日计划和执行跟踪 |
| **ai-daily-digest** | 从 90+ 个 AI/科技博客获取 RSS 订阅，生成每日摘要 |
| **akshare-skill** | 使用 AkShare 库访问中国金融数据 |
| **alex-session-wrap-up** | 会话结束自动化，包含知识捕获 |
| **apipick-company-facts** | 公司事实和商业智能 |
| **bat-cat** | 增强的 cat 克隆，带有语法高亮和 Git 集成 |
| **charts** | 图表生成和可视化 |
| **code-review** | 系统化代码审查模式 |
| **code-simplifier** | 简化和重构代码以降低复杂度 |
| **etf-assistant** | ETF 投资助理（沪深 300、创业板、科创 50、纳指等） |
| **pr-review** | 自动化 Pull Request 审查，集成 GitHub |
| **research-cog** | 由 CellCog 驱动的深度研究 Agent（DeepResearch Bench 第 1 名） |
| **security-auditor** | 代码库的全面安全审计 |
| **skill-creator** | 创建或更新 AgentSkills |
| **summarize** | 总结 URL 或文件（网页、PDF、图片、音频、YouTube） |
| **test-case-generator** | 测试用例生成工具 |
| **xiaohongshu-mcp** | 小红书 MCP 集成 |

---

## License / 许可证

- **Original skills** in `original/` directory: © 2026 lizhuojun. All rights reserved.
- **Open-source skills** in `opensource/` directory: Respective licenses apply (check individual skill directories).

- **`original/`目录中的原创技能**：© 2026 lizhuojun. 保留所有权利。
- **`opensource/`目录中的开源技能**：适用各自许可证（检查各个技能目录）。
