#!/usr/bin/env python3
import os, json, urllib.request

for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(k, None)

token = "8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY"
msg = """【晨报】美股收盘 + AI热点 | 2026-04-13

▌美股收盘（4月13日 周一）
来源：WLLS.com / Sharecafe / Trading Economics（2026-04-13，近24h）
- 道指：47,916.57，-269.23 点（-0.56%）
- 标普500：6,816.89，-7.77（-0.11%）
- 纳指：22,902.89，+80.48（+0.35%），科技股逆势撑场
- 领跌：Verizon(-3.62%)、Salesforce(-3.43%)、Nike(-3.14%)
- 领涨：Nvidia(+2.58%)、Amazon(+2.05%)、Caterpillar(+0.43%)

▌地缘与周一盘前背景
来源：CNBC / Yahoo Finance（2026-04-13，近2h）
- 美伊和平谈判破裂，霍尔木兹海峡封锁风险升温
- WTI原油亚盘涨超1%，亚洲市场普跌
- 道指期货亚盘跌约254点（-0.53%），标普期货-0.59%
- 避险情绪回升，能源股强势、科技股分化

▌AI热点 24h（2026-04-12~13）
来源：The Guardian / The Verge / Tradingkey / Business Insider（近24h）

1. 【Anthropic 自研芯片：或冲击 Nvidia 供应格局】
   Tradingkey 报道，Anthropic 正在考虑自研 AI 芯片，以缓解算力瓶颈并提升对成本和时间的自主控制。同时间亚马逊也在推进类似计划。算力自主化趋势若成，将对 Nvidia GPU 需求预期产生结构性影响。（来源：Tradingkey，2026-04-12）

2. 【The Guardian：Anthropic "安全" 理由遭质疑】
   Guardian 长文剖析 Anthropic 不发布 Claude Mythos Preview 的决定，称部分业内人士认为是营销噱头而非真正的安全顾虑。Anthropic 同时宣布 Project Glasswing——与微软、苹果、亚马逊、Google 组成网络防御联盟。（来源：The Guardian，2026-04-12）

3. 【The Verge：AI 代码战升温，Claude Code Moment 来袭】
   Verge 专栏指出 Anthropic 近期"有效封禁 OpenClaw"，四大厂商正在加速关闭生态开放入口，将开发者重新拉回各自闭环。AI 代码工具战争进入生态争夺阶段。（来源：The Verge，2026-04-13）

4. 【四大科技公司 AI 投入 $6000亿+，Anthropic 年化收入 $300亿】
   亚马逊、谷歌、微软、Meta 2026年AI投入合计已超 $6000亿；Anthropic 年化收入达 $300亿（同比增长3倍）；Google-Broadcom 新增大规模算力合作。（来源：Apple Podcasts，2026-04-12）

5. 【AI爬虫乱象持续：Anthropic 最严重（8800:1）】
   Business Insider 数据：Anthropic 每带来1次用户推荐，爬取网页 8,800次；OpenAI 为 993:1，内容版权争议持续发酵。（来源：Business Insider，2026-04-12）

▌简评
美股：周一在地缘风险下小幅收跌，纳指逆势小涨反映科技韧性与避险分化。中东局势是当前市场核心驱动，油价和波动率预计维持高位。
AI：Anthropic 自研芯片是最值得关注的长期变量——若成，Nvidia 替代逻辑弱化；代码生态争夺战正在加速，开放 vs 封闭的格局演变是今年主轴之一。

⚠️ 本简报仅供参考，不构成投资建议。"""

data = json.dumps({"chat_id": "7107266459", "text": msg}).encode("utf-8")
req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        print("OK:", r.read().decode())
except Exception as e:
    print("ERROR:", e)
