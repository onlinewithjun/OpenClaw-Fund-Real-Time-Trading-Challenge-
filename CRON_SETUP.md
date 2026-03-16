# 股市盯盘 Cron 配置

## 定时任务配置

将以下内容添加到 OpenClaw 配置或使用 `openclaw cron` 命令添加：

### 每 10 分钟盯盘（连续 3 次）

```bash
# 添加定时任务
openclaw cron add --schedule "*/10 * * * *" --task "
搜索最新股市行情并发送报告
"
```

## 手动执行盯盘

运行以下命令立即执行一次盯盘：

```bash
cd C:\Users\Administrator\.openclaw\workspace
py -3.14 market_monitor.py
```

## 使用 OpenClaw 会话发送

```bash
# 发送行情搜索请求到主会话
openclaw sessions_send --message "请帮我搜索当前股市行情：上证指数、深证成指、科创 50、创业板指、黄金、纳斯达克"
```

## 数据源说明

由于网络防火墙限制：
- **A 股实时数据**：无法直接访问新浪财经/东方财富 API
- **全球市场数据**：yfinance 可获取（但有延迟）
- **推荐方案**：使用 OpenClaw web_search 搜索最新行情新闻

## 替代方案

在聊天中直接发送以下指令，让我帮您搜索行情：

```
帮我查一下现在的股市行情
```

我会使用 web_search 获取最新数据并生成报告。
