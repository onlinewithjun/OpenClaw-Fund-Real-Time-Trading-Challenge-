# Agents Directory

**Purpose:** Configuration and orchestration for multi-agent architecture.

---

## 📂 Directory Structure

```
agents/
├── code-agent/
│   └── AGENTS.md          # Code agent configuration
├── finance-agent/
│   └── AGENTS.md          # Finance agent configuration
├── ops-agent/
│   └── AGENTS.md          # Ops agent configuration
├── CROSS_AGENT_CALLS.md   # Cross-agent call examples
├── ROUTING_CONFIG.md      # Gateway routing configuration
└── README.md              # This file
```

---

## 🎯 Agent Overview

| Agent | Skills | Model | Risk | Cron |
|-------|--------|-------|------|------|
| **Code** | 15 | openai-codex/gpt-5.4 | High | 0 |
| **Finance** | 24 | minimax/MiniMax-M2.5 | Low | 14 |
| **Ops** | 13 | minimax/MiniMax-M2.5 | Medium | 10 |

---

## 🚀 Quick Start

### Use Code Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="写一个 Python 脚本",
    streamTo="parent"
)
```

### Use Finance Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="查询基金 020899 的最新净值",
    streamTo="parent"
)
```

### Use Ops Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="ops-agent",
    task="清理 memory 文件",
    streamTo="parent"
)
```

---

## 📋 Current Status

### Phase 1: Logical Separation ✅ (Complete)
- Skills organized into `skills/code/`, `skills/finance/`, `skills/ops/`
- `AGENTS.md` updated with routing rules
- `skills/INDEX.md` created

### Phase 2: Physical Separation ✅ (Complete)
- `agents/` directory created
- Per-agent `AGENTS.md` configurations
- Cross-agent call examples documented
- Routing configuration documented

### Phase 3: Runtime Separation 🔄 (Planned)
- Gateway-level routing implementation
- Intent detection (keyword + context)
- Cross-agent call metrics
- Performance optimization

---

## 🔧 Configuration Files

### `code-agent/AGENTS.md`
- Skills: 15 (code development, testing, automation)
- Model: `openai-codex/gpt-5.4`
- Risk tolerance: High
- Cron tasks: 0

### `finance-agent/AGENTS.md`
- Skills: 24 (fund challenge, AlphaEar, news)
- Model: `minimax/MiniMax-M2.5`
- Risk tolerance: Low (read-only)
- Cron tasks: 14

### `ops-agent/AGENTS.md`
- Skills: 13 (maintenance, search, memory)
- Model: `minimax/MiniMax-M2.5`
- Risk tolerance: Medium
- Cron tasks: 10

---

## 📊 Usage

### Direct Session Spawn
```python
# Spawn a one-shot task
result = sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="生成今天的基金挑战日报",
    mode="run",
    streamTo="parent",
    timeoutSeconds=300
)
```

### Persistent Session
```python
# Start a persistent session
session = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="帮我开发一个功能",
    mode="session",
    streamTo="parent"
)
```

---

## 🔄 Cross-Agent Calls

See `CROSS_AGENT_CALLS.md` for detailed examples.

### Example: Finance → Code
```python
# Finance agent needs a scraper script
script = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="编写一个爬取天天基金网净值的 Python 脚本",
    streamTo="parent"
)
```

---

## 🧭 Routing

See `ROUTING_CONFIG.md` for routing configuration.

### Keyword Routing
| Keywords | Agent |
|----------|-------|
| `代码` `脚本` `测试` | Code |
| `基金` `股票` `净值` | Finance |
| `memory` `cron` `健康` | Ops |

---

## 📈 Metrics

Track agent usage in:
- `memory/code/usage.json`
- `memory/finance/usage.json`
- `memory/ops/usage.json`
- `memory/ops/cross-agent-calls.json`

---

## ⚠️ Important Notes

1. **Skills are shared** - All agents read from `skills/` directory
2. **Cron tasks unchanged** - Still run in main session
3. **Model selection** - Each agent uses domain-optimized model
4. **Risk tolerance** - Varies by agent (High/Medium/Low)

---

## 🚧 Future Work

### Phase 3: Runtime Separation
- [ ] Implement Gateway-level routing
- [ ] Add intent detection (keyword + ML)
- [ ] Create routing configuration file
- [ ] Test with 100+ sample queries
- [ ] Add routing metrics logging

### Phase 4: Optimization
- [ ] Performance benchmarking
- [ ] Cross-agent call caching
- [ ] Context window optimization
- [ ] User feedback integration

---

## 📚 Related Documents

- `AGENTS.md` - Main workspace configuration
- `skills/INDEX.md` - Skills index
- `SOUL.md` - Core identity
- `MEMORY.md` - Long-term memory
