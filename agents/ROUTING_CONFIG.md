# Gateway Routing Configuration (Phase 3 Prep)

This document describes the routing logic for Phase 3 (runtime separation).

---

## 🎯 Routing Architecture

```
User Input
    │
    ▼
┌─────────────────────────┐
│   Intent Detection      │
│   (Keyword + Context)   │
└─────────────────────────┘
    │
    ├─────────────┬─────────────┬─────────────┐
    │             │             │             │
    ▼             ▼             ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  Code   │ │ Finance │ │   Ops   │ │ Fallback│
│ Agent   │ │ Agent   │ │ Agent   │ │ (Ops)   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 📋 Keyword Routing Rules

### Route to Code Agent

| Keywords | Examples |
|----------|----------|
| `代码` `脚本` `程序` | "写一个 Python 脚本" |
| `测试` `unittest` `pytest` | "生成单元测试" |
| `PR` `review` `审查` | "review 这段代码" |
| `前端` `UI` `组件` | "创建一个 React 组件" |
| `浏览器` `爬取` `自动化` | "爬取这个网页" |
| `技能` `skill` `创建` | "创建一个新的 skill" |
| `git` `commit` `push` | "提交代码到 git" |
| `debug` `修复` `bug` | "修复这个 bug" |

### Route to Finance Agent

| Keywords | Examples |
|----------|----------|
| `基金` `净值` `持仓` | "今天基金收益如何" |
| `股票` `A 股` `美股` `港股` | "分析腾讯控股" |
| `盈亏` `收益` `回撤` | "计算今日盈亏" |
| `资讯` `新闻` `热点` | "推送 AI 热点 24h" |
| `ETF` `指数` | "推荐科技 ETF" |
| `买入` `卖出` `持仓` | "今天要不要加仓" |
| `挑战` `1000` `2000` | "基金挑战进展" |
| `A 股晚报` `港股晚报` | "推送 A 股晚报" |

### Route to Ops Agent

| Keywords | Examples |
|----------|----------|
| `内存` `memory` `归档` | "清理旧 memory 文件" |
| `cron` `定时` `任务` | "查看 cron 状态" |
| `健康` `检查` `状态` | "系统健康检查" |
| `技能` `安装` `发现` | "找一个天气技能" |
| `token` `使用` `报告` | "本周 token 使用报告" |
| `会话` `总结` `归档` | "总结这次会话" |
| `配置` `设置` `gateway` | "修改 gateway 配置" |

### Fallback to Ops Agent

If no keywords match:
- Greeting: "你好", "hello"
- General questions: "今天天气如何"
- Unknown intent: Route to Ops Agent

---

## 🧠 Context-Aware Routing

### Session History Matters

```python
# Example: User asks follow-up question
User: "基金挑战今天收益如何"  → Finance Agent
User: "那明天呢"              → Finance Agent (context)
User: "写个脚本自动获取"      → Code Agent (new intent)
```

### Implementation

```python
class Router:
    def __init__(self):
        self.last_domain = "ops"  # Default
        self.context_window = 5   # Last 5 messages
    
    def detect_intent(self, query, history):
        # 1. Check for explicit domain keywords
        domain = self.keyword_match(query)
        
        # 2. If unclear, check context
        if domain is None:
            domain = self.context_match(history)
        
        # 3. Fallback to last domain if still unclear
        if domain is None:
            domain = self.last_domain
        
        # 4. Update context
        self.last_domain = domain
        
        return domain
```

---

## 📝 Routing Configuration (JSON)

```json
{
  "routing": {
    "code-agent": {
      "keywords": ["代码", "脚本", "测试", "PR", "review", "前端", "浏览器", "爬取", "技能", "git", "debug"],
      "model": "openai-codex/gpt-5.4",
      "risk_tolerance": "high",
      "skills_path": "skills/code/"
    },
    "finance-agent": {
      "keywords": ["基金", "股票", "净值", "持仓", "盈亏", "资讯", "新闻", "ETF", "买入", "卖出", "挑战", "A 股", "美股", "港股"],
      "model": "bailian/qwen3.5-plus",
      "risk_tolerance": "low",
      "skills_path": "skills/finance/",
      "cron_tasks": 14
    },
    "ops-agent": {
      "keywords": ["内存", "memory", "cron", "健康", "检查", "技能", "安装", "token", "会话", "配置"],
      "model": "bailian/qwen3.5-plus",
      "risk_tolerance": "medium",
      "skills_path": "skills/ops/",
      "cron_tasks": 10,
      "is_fallback": true
    }
  },
  "context": {
    "window_size": 5,
    "stickiness_ms": 300000  // 5 minutes stick to same domain
  }
}
```

---

## 🔧 Implementation Options

### Option 1: Gateway-Level Routing (Recommended)

Modify OpenClaw Gateway to support domain routing:

```yaml
# config.yaml
multi_agent:
  enabled: true
  domains:
    - name: code-agent
      skills: skills/code/
      model: openai-codex/gpt-5.4
    - name: finance-agent
      skills: skills/finance/
      model: bailian/qwen3.5-plus
    - name: ops-agent
      skills: skills/ops/
      model: bailian/qwen3.5-plus
  routing:
    mode: keyword  # keyword | ml | hybrid
    fallback: ops-agent
```

### Option 2: Session-Level Routing

Use `sessions_spawn` for routing:

```python
# In main session
def handle_user_message(query):
    domain = detect_domain(query)
    result = sessions_spawn(
        runtime="subagent",
        agentId=f"{domain}-agent",
        task=query,
        streamTo="parent"
    )
    return result
```

### Option 3: Skill-Based Routing

Create a `router` skill that handles domain detection:

```python
# skills/ops/router/__init__.py
def route_query(query):
    domain = detect_domain(query)
    return f"Routing to {domain}-agent"
```

---

## 🧪 Testing Plan

### Test 1: Keyword Routing

```python
test_cases = [
    ("写一个 Python 脚本", "code-agent"),
    ("基金挑战今天收益如何", "finance-agent"),
    ("清理 memory 文件", "ops-agent"),
    ("你好", "ops-agent"),  # Fallback
]

for query, expected in test_cases:
    result = detect_domain(query)
    assert result == expected, f"Failed: {query}"
```

### Test 2: Context Routing

```python
# User asks follow-up without keywords
history = ["基金挑战今天收益如何"]  # Finance context
query = "那明天呢"  # No domain keywords
result = detect_domain(query, history)
assert result == "finance-agent"
```

### Test 3: Cross-Agent Call

```python
# Finance agent needs code help
result = sessions_spawn(
    runtime="subagent",
    agentId="code-agent",
    task="写一个爬取基金净值的脚本",
    streamTo="parent"
)
assert result is not None
```

---

## 📊 Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| Routing Accuracy | % of correct domain assignments | >95% |
| Avg Response Time | Time from query to response | <5s |
| Cross-Agent Calls | # of calls between agents | Track trend |
| Fallback Rate | % of queries routed to fallback | <10% |

---

## ⚠️ Edge Cases

### 1. Multi-Domain Query

```
User: "写个脚本爬取基金净值"
→ Contains both "脚本" (code) and "基金" (finance)
→ Decision: Route to Code Agent (action-oriented)
→ Code Agent can call Finance Agent for data
```

### 2. Ambiguous Query

```
User: "分析一下"
→ No domain keywords
→ Check context (last domain)
→ If no context, fallback to Ops Agent
```

### 3. Domain Switch

```
User: "基金挑战今天收益如何"  → Finance
User: "写个脚本自动化"        → Code (explicit switch)
User: "收益数据呢"             → Finance (back to previous)
```

---

## 🚀 Phase 3 Checklist

- [ ] Implement keyword detection function
- [ ] Add context-aware routing
- [ ] Create routing configuration file
- [ ] Test with 100+ sample queries
- [ ] Add routing metrics logging
- [ ] Document edge cases
- [ ] Create fallback handling
- [ ] Test cross-agent calls
- [ ] Performance optimization
- [ ] User documentation

---

## 📚 Related Documents

- `AGENTS.md` - Main workspace configuration
- `agents/*/AGENTS.md` - Per-agent configuration
- `CROSS_AGENT_CALLS.md` - Cross-agent call examples
- `skills/INDEX.md` - Skills index
