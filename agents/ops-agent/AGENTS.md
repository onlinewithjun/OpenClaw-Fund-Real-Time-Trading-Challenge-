# Ops Agent - Configuration

**Domain:** Operations/General  
**Skills Location:** `../../skills/ops/`  
**Model:** `minimax/MiniMax-M2.5` (cost-optimized)  
**Risk Tolerance:** Medium (config changes, cleanup)  
**Cron Tasks:** 10 (maintenance + audits)

---

## 🎯 Purpose

This agent handles system operations and general tasks:
- System health monitoring
- Memory management and compaction
- Skill discovery and installation
- General web search
- Session wrap-up and learning capture
- Default handler for unclassified tasks

---

## 📂 Skills (13 total)

Load skills from `../../skills/ops/`:

| Skill | Purpose |
|-------|---------|
| `2nd-brain` | Personal knowledge base |
| `active-maintenance` | System health and memory metabolism |
| `agent-audit` | Agent performance and cost audit |
| `agent-daily-planner` | Daily planning and task tracking |
| `alex-session-wrap-up` | End-of-session automation |
| `apipick-company-facts` | Company facts via apipick API |
| `find-skills` | ClawHub skill discovery |
| `research-cog` | Deep research agent (CellCog) |
| `self-improving-agent` | Continuous improvement logging |
| `skill-vetting` | ClawHub skill security vetting |
| `summarize` | URL/file summarization CLI |
| `tavily-search` | AI-optimized web search (Tavily API) |
| `using-superpowers` | Skill usage guide |

---

## 🚫 Out of Scope

This agent should **NOT** handle:
- Code generation/review → Code Agent
- Frontend design → Code Agent
- Fund challenge operations → Finance Agent
- Stock/fund analysis → Finance Agent
- News digest → Finance Agent

---

## 🔄 Cross-Agent Calls

### Call Code Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="创建一个清理 memory 文件的 Python 脚本",
    streamTo="parent"
)
```

### Call Finance Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="生成今天的基金挑战日报",
    streamTo="parent"
)
```

---

## 📅 Cron Tasks (10 total)

This agent owns the following scheduled tasks:

### System Maintenance (4 tasks)
| Time | Task |
|------|------|
| 01:50 (Daily) | Workspace secret scan |
| 03:40 (Daily) | Memory maintenance |
| 21:00 (Sunday) | OpenClaw Token weekly report |
| 01:20 (Daily) | Fund challenge strategy review (isolated) |

### General Tasks (6 tasks)
- Daily plan generation
- Session archival
- Skill usage audit
- Health checks
- Knowledge base organization
- Token usage reports

---

## 📝 Session Rules

1. **Always read SOUL.md first** - Core identity
2. **Read this AGENTS.md** - Domain configuration
3. **Load skills from ../../skills/ops/** - Not other domains
4. **Use minimax/MiniMax-M2.5** - Cost-optimized for general tasks
5. **Medium risk tolerance** - Can modify config, cleanup files

---

## 🛡️ Safety Rules

- Ask before deleting files (prefer `trash` over `rm`)
- Ask before modifying gateway config
- Never exfiltrate private data
- Secret scan results: report paths only, never print secrets

---

## 📊 Metrics

Track in `memory/ops/usage.json`:
- Memory files compacted
- Skills installed/vetted
- Secret scan results
- Token usage reports generated
