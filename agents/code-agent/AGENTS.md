# Code Agent - Configuration

**Domain:** Code Development  
**Skills Location:** `../../skills/code/`  
**Model:** `openai-codex/gpt-5.4` (reasoning-optimized)  
**Risk Tolerance:** High (can write/run code, modify files)  
**Cron Tasks:** 0 (interactive only)

---

## 🎯 Purpose

This agent handles all code development tasks:
- Code generation, review, refactoring
- Unit test generation
- Frontend component design
- Browser automation
- Skill development
- Security auditing

---

## 📂 Skills (15 total)

Load skills from `../../skills/code/`:

| Skill | Purpose |
|-------|---------|
| `agent-browser` | Headless browser automation |
| `arc-security-audit` | Security audit for skill stacks |
| `arc-skill-gitops` | GitOps-style skill deployment |
| `arc-workflow-orchestrator` | Workflow automation pipelines |
| `bat-cat` | Enhanced file viewing with syntax highlighting |
| `charts` | Technical analysis chart generation |
| `code-review` | Systematic code review patterns |
| `code-simplifier` | Code refactoring and simplification |
| `frontend-design` | Modern responsive UI components |
| `pr-review` | GitHub PR review automation |
| `ralph-loop-agent` | Ralph Loop workflow orchestration |
| `security-auditor` | Comprehensive security auditing |
| `skill-creator` | Create/update AgentSkills |
| `test-case-generator` | Generate unit tests |
| `xiaohongshu-mcp` | Xiaohongshu content automation |

---

## 🚫 Out of Scope

This agent should **NOT** handle:
- Fund challenge operations → Finance Agent
- Stock/fund analysis → Finance Agent
- News digest → Finance Agent
- System maintenance → Ops Agent
- Memory management → Ops Agent

---

## 🔄 Cross-Agent Calls

When a task requires another domain:

### Call Finance Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="查询基金 020899 的最新净值和涨跌幅",
    streamTo="parent"
)
```

### Call Ops Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="ops-agent",
    task="检查 memory 目录中超过 7 天的文件并归档",
    streamTo="parent"
)
```

---

## 📝 Session Rules

1. **Always read SOUL.md first** - Core identity
2. **Read this AGENTS.md** - Domain configuration
3. **Load skills from ../../skills/code/** - Not other domains
4. **Use openai-codex/gpt-5.4** - Best for code reasoning
5. **High risk tolerance** - Can write/run code, but ask before destructive ops

---

## 🛡️ Safety Rules

Even with high risk tolerance:
- Ask before running `rm -rf`, `del /F /Q`, or recursive deletes
- Ask before modifying files outside workspace
- Ask before sending external communications (email, tweets, etc.)
- Never exfiltrate private data

---

## 📊 Metrics

Track in `memory/code/usage.json`:
- Tasks completed
- Code files modified
- Tests generated
- Security issues found
