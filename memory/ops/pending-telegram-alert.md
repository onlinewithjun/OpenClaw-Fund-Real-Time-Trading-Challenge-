# 安全告警待发送 — Telegram 7107266459

**时间**: 2026-04-05 01:50 (UTC+8)
**状态**: 待发送
**优先级**: 🔴 极高

## 告警内容（中文，纯文本）

```
🔴 安全扫描报告 — 2026-04-05

🚨 高危：凭证已推送至 GitHub 公开仓库！

📁 受影响文件：
skills/code/xiaohongshu-mcp/cookies.json

该文件已确认存在于 GitHub 远程仓库：
https://github.com/onlinewithjun/OpenClaw-Fund-Real-Time-Trading-Challenge-

包含内容：小红书 web_session、id_token、websectiga、acw_tc 等多枚真实认证 Cookies。
这些 Cookie 可被他人用于直接登录你的小红书账号！

✅ 已执行：incident 已记录至 memory/2026-04-05.md

🔴 立即行动：
1. 小红书 App → 退出所有设备登录（强制刷新 session）
2. 浏览器重新扫码登录
3. 联系 GitHub Support 请求清除敏感数据：
   https://github.com/onlinewithjun/OpenClaw-Fund-Real-Time-Trading-Challenge-/security/advisories/new
4. 本地清理 git 历史：
   git filter-repo --path skills/code/xiaohongshu-mcp/cookies.json --invert-paths --force
   git push origin --force --all
5. 确认 .gitignore 排除 cookies.json，重新提交
```

**说明**：Telegram bot token 在 isolated cron session 中不可访问（OpenClaw 加密存储），
请由 main session 或人工发送以上内容至 Telegram 7107266459。
