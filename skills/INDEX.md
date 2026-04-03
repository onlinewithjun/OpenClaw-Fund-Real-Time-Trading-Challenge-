# Skills Index

**Last Updated:** 2026-03-16  
**Total Skills:** 50 (Code: 15, Finance: 21, Ops: 14)

---

## 📂 Directory Structure

```
skills/
├── code/           # Code Development Domain (15 skills)
├── finance/        # Finance/Investment Domain (21 skills)
└── ops/            # Operations/General Domain (14 skills)
```

---

## 🔧 Code Domain (15 skills)

**Purpose:** Code generation, review, testing, automation, and development workflows.

**Model:** `openai-codex/gpt-5.4` (reasoning-optimized)  
**Risk Tolerance:** High (can write/run code, modify files)  
**Cron Tasks:** 0 (interactive only)

| Skill | Description | Usage |
|-------|-------------|-------|
| `agent-browser` | Headless browser automation | Web scraping, UI testing |
| `arc-security-audit` | Security audit for skill stacks | Security review |
| `arc-skill-gitops` | GitOps-style skill deployment | CI/CD for skills |
| `arc-workflow-orchestrator` | Workflow automation pipelines | Multi-skill orchestration |
| `bat-cat` | Enhanced `cat` with syntax highlighting | File viewing |
| `charts` | Technical analysis chart generation | Finance charts |
| `code-review` | Systematic code review patterns | PR review, code quality |
| `code-simplifier` | Code refactoring and simplification | Reduce complexity |
| `frontend-design` | Modern responsive UI components | React/Vue/Angular |
| `pr-review` | GitHub PR review automation | Code review workflow |
| `ralph-loop-agent` | Ralph Loop workflow orchestration | Coding agent loops |
| `security-auditor` | Comprehensive security auditing | Vulnerability detection |
| `skill-creator` | Create/update AgentSkills | Skill development |
| `test-case-generator` | Generate unit tests | Testing automation |
| `xiaohongshu-mcp` | Xiaohongshu content automation | Social media ops |

---

## 📈 Finance Domain (21 skills)

**Purpose:** Fund challenge operations, stock analysis, news aggregation, investment research.

**Model:** `minimax/MiniMax-M2.5` (analysis-optimized)  
**Risk Tolerance:** Low (read-only, no auto-trade)  
**Cron Tasks:** 14 (fund challenge + news digest)

### Fund Challenge (12 skills)

| Skill | Description | Usage |
|-------|-------------|-------|
| `fund-challenge-daily-trader-core` | End-to-end daily trading workflow | Daily operations |
| `fund-challenge-data-guard` | Data integrity anti-hallucination | Data validation |
| `fund-challenge-evidence-audit` | Evidence capture and decision gating | Audit trail |
| `fund-challenge-execution-engine` | Execution and risk engine | Trade execution |
| `fund-challenge-identity-freshness-guard` | Fund code-name verification | Identity check |
| `fund-challenge-instrument-rules` | Per-fund trading rule resolver | Rule enforcement |
| `fund-challenge-ledger-postmortem` | State persistence and ledger audit | Post-trade review |
| `fund-challenge-market-calendar-gate` | Trading-day and cut-off gate | Calendar validation |
| `fund-challenge-offexchange-exec-sim` | Off-exchange execution simulator | T+ simulation |
| `fund-challenge-orchestrator` | Master orchestrator | Workflow coordination |
| `fund-challenge-position-risk-engine` | Position sizing and risk control | Risk management |
| `fund-challenge-signal-fusion-engine` | Short-term signal fusion | Signal aggregation |

### AlphaEar Finance (9 skills)

| Skill | Description | Usage |
|-------|-------------|-------|
| `ai-daily-digest` | AI/tech blog RSS aggregation (90+ sources) | Daily digest |
| `akshare-skill` | Chinese financial data access (AkShare) | A-share/HK/US data |
| `alphaear-deepear-lite` | DeepEar Lite financial signals | Signal fetching |
| `alphaear-logic-visualizer` | Finance logic diagram generation | Visualization |
| `alphaear-news` | Hot finance news aggregation | News fetching |
| `alphaear-predictor` | Market prediction (Kronos model) | Time-series forecast |
| `alphaear-reporter` | Financial report generation | Report writing |
| `alphaear-search` | Finance web search + local RAG | Finance search |
| `alphaear-sentiment` | Finance text sentiment analysis (FinBERT) | Sentiment scoring |
| `alphaear-signal-tracker` | Investment signal evolution tracking | Signal monitoring |
| `alphaear-stock` | A-Share/HK/US stock ticker search | Stock data |
| `etf-assistant` | ETF investment assistant | ETF queries |

---

## ⚙️ Ops Domain (14 skills)

**Purpose:** System maintenance, memory management, skill discovery, general utilities.

**Model:** `minimax/MiniMax-M2.5` (cost-optimized)  
**Risk Tolerance:** Medium (config changes, cleanup)  
**Cron Tasks:** 10 (maintenance + audits)

| Skill | Description | Usage |
|-------|-------------|-------|
| `2nd-brain` | Personal knowledge base | Knowledge capture |
| `active-maintenance` | System health and memory metabolism | Auto-maintenance |
| `agent-audit` | Agent performance and cost audit | ROI analysis |
| `agent-daily-planner` | Daily planning and task tracking | Productivity |
| `alex-session-wrap-up` | End-of-session automation | Session summary |
| `apipick-company-facts` | Company facts via apipick API | Company lookup |
| `find-skills` | ClawHub skill discovery | Skill installation |
| `research-cog` | Deep research agent (CellCog) | Research tasks |
| `self-improving-agent` | Continuous improvement logging | Learning capture |
| `skill-vetting` | ClawHub skill security vetting | Security review |
| `summarize` | URL/file summarization CLI | Content summary |
| `tavily-search` | AI-optimized web search (Tavily API) | General search |
| `using-superpowers` | Skill usage guide | Onboarding |

---

## 🔄 Cross-Domain Calls

When a task requires cross-domain collaboration:

1. **Identify primary domain** based on user intent
2. **Use `sessions_spawn`** to call the other domain agent
3. **Example:** Finance agent needs to write code → spawn Code agent

```python
# Example: Finance → Code call
sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="编写爬取基金净值的 Python 脚本",
    streamTo="parent"
)
```

---

## 📊 Usage Tracking

**Track skill usage in:** `memory/ops/skill-usage.json`

```json
{
  "lastUpdated": "2026-03-16",
  "skills": {
    "code-review": {"count": 15, "lastUsed": "2026-03-15"},
    "alphaear-news": {"count": 30, "lastUsed": "2026-03-16"}
  }
}
```

---

## 🗑️ Archived Skills

Skills moved to `skills/archive/` (inactive > 90 days):

| Skill | Archived Date | Reason |
|-------|---------------|--------|
| (none yet) | - | - |

---

## 📝 Notes

- **Skill locations:** All skills are now organized by domain in `skills/{code,finance,ops}/`
- **Original paths:** Old paths (`skills/opensource/`, `skills/original/`) have been removed
- **Backward compatibility:** Update any hardcoded skill paths in scripts
- **Adding new skills:** Place in the appropriate domain folder based on purpose
