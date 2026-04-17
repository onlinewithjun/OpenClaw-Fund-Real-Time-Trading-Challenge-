#!/usr/bin/env python3
import os, json, urllib.request, urllib.parse

# Clear proxy env
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(k, None)

token = "8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY"
chat_id = "7107266459"

msg = """【晨报】美股收盘 + AI热点 | 2026-04-13

▌美股收盘（4月11日 周六休市 / 4月10日周四收盘）
来源：Yahoo Finance / Trading Economics（2026-04-10 近24h）
- 道指：47,917 点，-269 点（-0.56%），连跌两日
- 标普500：6,816.89，-7.77（-0.11%），连续第7日上涨（2025年10月以来最长连胜）
- 纳指：近持平，科技股分化
- 领跌股：Verizon(-3.62%)、Salesforce(-3.43%)、Nike(-3.14%)
- 领涨股：Nvidia(+2.58%)、Amazon(+2.05%)、Caterpillar(+0.43%)
- 本周总结：受中东局势缓解预期提振，前四日反弹，周五回吐部分涨幅

▌周一盘前预警（4月13日 周一）
来源：CNBC TV18 / Yahoo Finance（2026-04-13 近2h）
- 美伊和平谈判在伊斯兰堡破裂，霍尔木兹海峡遭封锁
- WTI原油暴涨 +8%至 $104.62
- 道指期货下跌约550点（-1.2%），标普500期货-80点，纳指期货-320点
- 风险提示：地缘政治驱动波动性上升，能源板块可能跳空高开

▌AI热点 24h（2026-04-12~13）
来源：Reuters / The Atlantic / Business Insider / Anthropic官方（近24h）

1. 【Anthropic 发布 Claude Mythos Preview】
   Anthropic 宣布前沿模型 Claude Mythos Preview，能力足以加速网络攻击，主动选择不公开发布。配套推出 Project Glasswing——联合微软、苹果、亚马逊、Google 四家巨头共同构建网络防御联盟。英国监管机构已介入评估风险。（来源：Reuters，2026-04-11）

2. 【OpenAI 收入预期：广告业务2026年达25亿美元】
   内部文件显示 OpenAI 预计2026年广告收入 $25亿，2030年有望突破 $1000亿/年，广告正成为其非ChatGPT业务的重要支柱。（来源：Wikipedia/OpenAI，2026-04-11）

3. 【AI爬虫乱象：Anthropic 最严重，比例达8800:1】
   研究数据显示，Anthropic爬虫网页8,800次才带来1次用户推荐流量；OpenAI紧随其后（993:1），大量网站内容被AI无偿爬取引发版权争议。（来源：Business Insider，2026-04-11）

4. 【四大科技公司2026年AI投入合计超6000亿美元】
   亚马逊、谷歌、微软、Meta四家超大规模企业2026年已累计投入 $6000亿+用于AI建设；Anthropic年化收入达 $300亿（同比增长3倍）。（来源：Kevin MD / Podcasts，2026-04-11）

5. 【Google Gemma 4 强势崛起】
   Google Gemma 4 在开源社区快速传播，监管层面也在密切关注AI模型安全风险。（来源：Apple Podcasts，2026-04-11）

▌简评
美股：周五小幅收跌，周一盘前因地缘风险承压。中东谈判破裂提升避险情绪，能源股强、科技股分化。
AI：Anthropic "不出售安全" 的商业选择是本周最大变量——四巨头的 Glasswing 联盟值得持续关注。

⚠️ 本简报仅供参考，不构成投资建议。"""

data = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")
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
