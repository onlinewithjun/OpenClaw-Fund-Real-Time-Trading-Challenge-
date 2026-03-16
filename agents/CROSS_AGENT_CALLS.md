# Cross-Agent Call Examples

This document provides examples of how to call other agents from each domain.

---

## 📋 Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Gateway Layer                         │
│  (User input → Intent detection → Route to agent)       │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │  Code Agent   │ │ Finance Agent │ │   Ops Agent   │
    │               │ │               │ │               │
    │  ←───────→    │ │  ←───────→    │ │  ←───────→    │
    │  Cross-agent calls via sessions_spawn              │
    └───────────────┘ └───────────────┘ └───────────────┘
```

---

## 🔧 Code Agent → Other Agents

### Code → Finance: Query Fund Data

```python
# Task: Get latest NAV for fund 020899
result = sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="查询基金 020899 的最新净值、涨跌幅、持仓信息",
    mode="run",  # One-shot execution
    streamTo="parent",  # Stream results back
    timeoutSeconds=300
)
```

### Code → Ops: Memory Cleanup

```python
# Task: Archive old memory files
result = sessions_spawn(
    runtime="subagent",
    agentId="ops-agent",
    task="检查 memory/ 目录中超过 7 天的文件并移动到 memory/archive/",
    mode="run",
    streamTo="parent",
    timeoutSeconds=180
)
```

### Code → Finance: Generate Chart Data

```python
# Task: Get historical data for chart
result = sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="获取 020899 过去 30 天的净值数据，格式：日期，净值，涨跌幅",
    mode="run",
    streamTo="parent",
    timeoutSeconds=120
)
# Then use charts skill to visualize
```

---

## 📈 Finance Agent → Other Agents

### Finance → Code: Write Scraper Script

```python
# Task: Create a fund NAV scraper
script = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="""
编写一个爬取天天基金网净值的 Python 脚本：
- 输入：基金代码列表
- 输出：JSON 格式（代码，净值，日期，涨跌幅）
- 使用 requests 库
- 添加错误处理和重试逻辑
""",
    mode="run",
    streamTo="parent",
    timeoutSeconds=300
)
# Save script to fund_challenge/scripts/
```

### Finance → Code: Fix Bug in Script

```python
# Task: Debug a failing script
fix = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="""
修复 fund_challenge/scripts/state_refresh.py 的错误：
错误信息：ModuleNotFoundError: No module named 'xxx'
请检查导入语句并修复
""",
    mode="run",
    streamTo="parent",
    timeoutSeconds=180
)
```

### Finance → Ops: Update Usage Stats

```python
# Task: Log finance agent usage
result = sessions_spawn(
    runtime="subagent",
    agentId="ops-agent",
    task="更新 memory/finance/usage.json，记录今日决策次数和新闻推送数",
    mode="run",
    streamTo="parent",
    timeoutSeconds=60
)
```

---

## ⚙️ Ops Agent → Other Agents

### Ops → Code: Generate Maintenance Script

```python
# Task: Create a cleanup script
script = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="""
创建一个清理 workspace 临时文件的 Python 脚本：
- 删除 *.tmp, *.bak, *.log (超过 7 天)
- 删除 __pycache__ 目录
- 删除 .pytest_cache 目录
- 生成清理报告
""",
    mode="run",
    streamTo="parent",
    timeoutSeconds=240
)
```

### Ops → Finance: Get Token Usage Report

```python
# Task: Generate weekly token report
report = sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="""
生成 OpenClaw Token 使用周报：
- 本周输入/输出 token 总数
- Cron 任务 token 消耗占比
- Top 3 高消耗任务
- 与上周对比
""",
    mode="run",
    streamTo="parent",
    timeoutSeconds=180
)
```

### Ops → Code: Security Scan

```python
# Task: Scan for secrets
result = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="""
扫描 workspace 中的敏感信息：
- Telegram bot tokens
- API keys
- GitHub tokens
- Private keys
发现后报告文件路径（不要打印具体值）
""",
    mode="run",
    streamTo="parent",
    timeoutSeconds=300
)
```

---

## 🔄 Bidirectional Call Patterns

### Pattern 1: Request-Response

```python
# Caller (any agent)
result = sessions_spawn(
    runtime="subagent",
    agentId="target-agent",
    task="Specific task description",
    mode="run",
    streamTo="parent"
)
# Process result in caller
```

### Pattern 2: Streaming Results

```python
# Caller (any agent)
result = sessions_spawn(
    runtime="subagent",
    agentId="target-agent",
    task="Long-running task",
    mode="session",  # Persistent session
    streamTo="parent",
    timeoutSeconds=600
)
# Results stream as they arrive
```

### Pattern 3: Chained Calls

```python
# Ops agent needs data from Finance, then code from Code
finance_data = sessions_spawn(
    runtime="subagent",
    agentId="finance-agent",
    task="Get fund challenge NAV data",
    mode="run",
    streamTo="parent"
)

code_script = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task=f"Create chart script using this data: {finance_data}",
    mode="run",
    streamTo="parent"
)
```

---

## ⚠️ Best Practices

### 1. Keep Tasks Specific
❌ Bad: "Help with finance stuff"  
✅ Good: "查询基金 020899 的最新净值和涨跌幅"

### 2. Set Appropriate Timeouts
- Simple queries: 60-120 seconds
- Code generation: 180-300 seconds
- Complex analysis: 300-600 seconds

### 3. Use Correct Mode
- `mode="run"` - One-shot execution (default)
- `mode="session"` - Persistent session for multi-turn

### 4. Stream Results
- Always use `streamTo="parent"` to get results
- Results appear in parent session's next message

### 5. Handle Errors
```python
try:
    result = sessions_spawn(...)
except Exception as e:
    # Fallback or user notification
    print(f"Cross-agent call failed: {e}")
```

---

## 📊 Call Metrics

Track cross-agent calls in `memory/ops/cross-agent-calls.json`:

```json
{
  "date": "2026-03-16",
  "calls": [
    {"from": "finance", "to": "code", "task": "scraper", "duration_ms": 15234},
    {"from": "ops", "to": "finance", "task": "token_report", "duration_ms": 8921}
  ],
  "total_calls": 2,
  "avg_duration_ms": 12077
}
```

---

## 🧪 Testing Cross-Agent Calls

### Test 1: Finance → Code
```bash
# In finance-agent session
python -c "
from openclaw import sessions_spawn
result = sessions_spawn(
    runtime='subagent',
    agentId='code-agent',
    task='Write a hello world Python function',
    mode='run',
    streamTo='parent'
)
print(result)
"
```

### Test 2: Code → Finance
```bash
# In code-agent session
python -c "
from openclaw import sessions_spawn
result = sessions_spawn(
    runtime='subagent',
    agentId='finance-agent',
    task='查询基金 020899 的最新净值',
    mode='run',
    streamTo='parent'
)
print(result)
"
```

### Test 3: Ops → Both
```bash
# In ops-agent session
# Test calls to both code and finance agents
```

---

## 🔍 Debugging

### Issue: Call times out
- Check agentId is correct
- Increase timeoutSeconds
- Verify target agent skills are loaded

### Issue: No results returned
- Ensure `streamTo="parent"` is set
- Check sessions_spawn returned without error
- Verify task description is clear

### Issue: Wrong agent responds
- Check routing logic in Gateway
- Verify agentId matches configuration
- Ensure skills are in correct domain folder
