# 多 Agent 配置应用指南

**创建日期:** 2026-03-16  
**适用版本:** OpenClaw 2026.3.x+

---

## 🎯 目标

在 OpenClaw Dashboard 中显示 4 个独立 Agent 实例：
- `main-agent` - 主 Agent（路由 + 通用任务）
- `code-agent` - 代码开发
- `finance-agent` - 金融投资
- `ops-agent` - 系统运维

---

## 📋 方案对比

### 方案一：配置多 Agent Profiles（推荐）⭐

**优点:**
- Dashboard 显示所有 Agent
- 每个 Agent 独立配置（模型/技能/风险容忍）
- Cron 任务可绑定到特定 Agent
- 用户可直接选择与哪个 Agent 对话

**缺点:**
- 需要重启 Gateway
- 占用更多资源（4 个常驻 Agent）

**适用场景:** 生产环境，需要清晰的多 Agent 界面

---

### 方案二：动态 Subagent（当前实现）

**优点:**
- 无需修改配置
- 资源按需分配
- 与现有 cron 兼容

**缺点:**
- Dashboard 不显示 subagent
- 每次创建有启动开销
- 用户感知不到多 Agent 存在

**适用场景:** 开发测试，临时任务

---

## 🔧 应用方案一（推荐）

### 步骤 1：备份当前配置

```powershell
Copy-Item ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```

### 步骤 2：应用配置补丁

**方式 A：使用 gateway 工具**
```python
# 在 OpenClaw 会话中
gateway(action="config.patch", patch={...})
```

**方式 B：手动编辑**
```bash
# 编辑配置文件
notepad ~/.openclaw/openclaw.json

# 添加 agents.list 配置（见下方）
```

### 步骤 3：重启 Gateway

```powershell
openclaw gateway restart
```

### 步骤 4：验证

打开 Dashboard，应该看到 4 个 Agent 实例：
- Main Agent
- Code Agent
- Finance Agent
- Ops Agent

---

## 📝 完整配置示例

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.4",
        "fallbacks": ["bailian/qwen3.5-plus"]
      },
      "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace",
      "timeoutSeconds": 900,
      "memorySearch": {
        "provider": "openai",
        "remote": {
          "baseUrl": "http://127.0.0.1:18890/v1",
          "apiKey": "__REDACTED__"
        },
        "fallback": "none",
        "model": "text-embedding-v4"
      }
    },
    "list": [
      {
        "id": "main-agent",
        "name": "Main Agent",
        "description": "默认主 Agent，处理通用任务和路由分发",
        "model": {
          "primary": "openai-codex/gpt-5.4",
          "fallbacks": ["bailian/qwen3.5-plus"]
        },
        "skills": {
          "load": ["skills/ops/"]
        },
        "timeoutSeconds": 900
      },
      {
        "id": "code-agent",
        "name": "Code Agent",
        "description": "代码开发 Agent - 代码生成/审查/测试/自动化",
        "model": {
          "primary": "openai-codex/gpt-5.4",
          "fallbacks": ["bailian/qwen3-coder-next"]
        },
        "skills": {
          "load": ["skills/code/"]
        },
        "timeoutSeconds": 900,
        "riskTolerance": "high"
      },
      {
        "id": "finance-agent",
        "name": "Finance Agent",
        "description": "金融投资 Agent - 基金挑战/股票分析/新闻资讯",
        "model": {
          "primary": "bailian/qwen3.5-plus",
          "fallbacks": ["openai-codex/gpt-5.4"]
        },
        "skills": {
          "load": ["skills/finance/"]
        },
        "timeoutSeconds": 900,
        "riskTolerance": "low",
        "cron": {
          "assign": [
            "基金挑战#01-健康检查",
            "基金挑战#02-扩池刷新",
            "资讯#01-美股收盘晨报",
            "资讯#02-AI 热点 24h",
            "资讯#03-A 股晚报",
            "资讯#04-港股晚报"
          ]
        }
      },
      {
        "id": "ops-agent",
        "name": "Ops Agent",
        "description": "运维 Agent - 系统维护/内存管理/技能发现",
        "model": {
          "primary": "bailian/qwen3.5-plus",
          "fallbacks": ["openai-codex/gpt-5.4"]
        },
        "skills": {
          "load": ["skills/ops/"]
        },
        "timeoutSeconds": 900,
        "riskTolerance": "medium",
        "cron": {
          "assign": [
            "Workspace secret scan",
            "Memory maintenance",
            "OpenClaw#01-周日 Token 使用报告"
          ]
        }
      }
    ]
  }
}
```

---

## 🔄 路由集成

应用多 Agent 配置后，路由脚本自动生效：

```python
# agents/router.py
router = AgentRouter()
domain = router.detect_domain(user_query)
# domain 将匹配配置的 agent ID: "code-agent", "finance-agent", etc.
```

---

## ⚠️ 注意事项

### 1. 资源占用
- 4 个常驻 Agent 会占用更多内存
- 每个 Agent 独立加载技能（约 50-100MB/个）
- 建议服务器内存 >= 8GB

### 2. Cron 迁移
- 现有 cron 任务仍在 main session 运行
- 需要更新 cron 配置，绑定到对应 Agent
- 示例：
  ```json
  "cron": {
    "assign": ["基金挑战#01-健康检查"]
  }
  ```

### 3. 会话隔离
- 每个 Agent 有独立的会话历史
- Memory 共享（通过 memory_search）
- 跨 Agent 调用仍需 `sessions_spawn`

### 4. 回滚方案
```powershell
# 如果出现问题，恢复备份配置
Copy-Item ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json
openclaw gateway restart
```

---

## 📊 Dashboard 效果

应用配置后，Dashboard 显示：

```
┌─────────────────────────────────────────────────────────┐
│  OpenClaw Dashboard                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🤖 Main Agent                                          │
│     状态：在线 | 模型：gpt-5.4 | 技能：13              │
│     最后活动：2 分钟前                                  │
│                                                         │
│  💻 Code Agent                                          │
│     状态：在线 | 模型：gpt-5.4 | 技能：15              │
│     最后活动：5 分钟前                                  │
│                                                         │
│  📈 Finance Agent                                       │
│     状态：在线 | 模型：qwen3.5-plus | 技能：24         │
│     最后活动：刚刚                                      │
│                                                         │
│  ⚙️ Ops Agent                                           │
│     状态：在线 | 模型：qwen3.5-plus | 技能：13         │
│     最后活动：1 分钟前                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速应用

**一键应用配置（推荐）:**

```powershell
# 1. 备份
Copy-Item ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 2. 在 OpenClaw 中执行
gateway(action="config.patch", patch={
  "agents": {
    "list": [
      {"id": "main-agent", "name": "Main Agent", ...},
      {"id": "code-agent", "name": "Code Agent", ...},
      {"id": "finance-agent", "name": "Finance Agent", ...},
      {"id": "ops-agent", "name": "Ops Agent", ...}
    ]
  }
}, note="多 Agent 配置已应用")

# 3. 重启
openclaw gateway restart
```

---

## 📚 相关文档

- `agents/routing.json` - 路由配置
- `agents/router.py` - 路由实现
- `agents/CROSS_AGENT_CALLS.md` - 跨 Agent 调用
- `MULTI_AGENT_ARCHITECTURE.md` - 架构总结

---

**最后更新:** 2026-03-16 19:30 (Asia/Shanghai)
