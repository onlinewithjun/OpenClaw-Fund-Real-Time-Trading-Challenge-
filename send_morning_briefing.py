import urllib.request
import json

BOT_TOKEN = "7816897827:AAFDiwioHWMm1RwDV7UuC3N3KNFVqDVF8gQ"
chat_id = "7107266459"

msg = """📊 【晨报】美股收盘 + AI热点 | 2026-04-17

━━━━━━━━━━━━━━━━━━━━
🌅 一、美股收盘
━━━━━━━━━━━━━━━━━━━━
📰 来源：CNBC / TheStreet / Bloomberg
🕐 数据时间：2026-04-16 美股收盘（约 21:00 UTC）

【市场概况】
标普500与纳斯达克综合指数周三（前一个收盘日）双双创下历史新高，周四（4/16）维持高位。纳斯达克连续第12个交易日上涨，创2009年7月以来最长连涨纪录。

主要指数：
• 标普500：≈7022.95（周三创历史收盘新高），周四期货约7068附近
• 纳斯达克100：创盘中历史新高
• 道琼斯：周三盘中历史新高后略有回落（约 -37点）
• 10年期美债收益率：约4.278%

【个股亮点】
• D-Wave Quantum（QBTS）：+3.41%，收于$21.52，因Nvidia量子AI概念再获关注
• 大型银行股：业绩显示消费端韧性，摩根大通等跑赢
• 科技权重股：苹果（-1.52%）、亚马逊（-1.48%）、波音（-1.99%）小幅回调

【宏观背景】
• 中东局势（美伊冲突）持续，但市场已消化利空，未现恐慌
• 油价上涨带来通胀担忧，但美股整体维持强势
• 亚马逊宣布以115.7亿美元收购卫星公司Globalstar，追赶SpaceX星链

━━━━━━━━━━━━━━━━━━━━
🤖 二、AI热点 24h
━━━━━━━━━━━━━━━━━━━━
📰 来源：澎湃新闻 / ThePaper / llm-stats.com / heise online
🕐 数据时间：2026-04-16

【重大发布】
1️⃣ OpenAI 发布 GPT-5.4-Cyber：专门面向网络安全领域的AI模型，与Anthropic的Mythos对标，初期限制访问
2️⃣ OpenAI 发布 GPT-Rosalind：首个生命科学方向AI模型，专注药物发现与基因组学研究
3️⃣ Anthropic 扩大与Google和Broadcom合作：用于下一代计算基础设施（多吉瓦级）

【GitHub 趋势】
• Voicebox：开源语音合成工作室项目，引发社区对透明语音生成技术的关注
• Ollama：持续更新，darwin版和Linux AMD ROCm版本发布

【国内动态】
• 腾讯宣布企业微信CLI项目（wecom-cli）正式开源，开放消息/日程/文档/会议等7大核心能力，支持Claude Code、QClaw等主流AI Agent调用
• 亚马逊115.7亿美元收购Globalstar：布局卫星网络追赶星链
• 锂电池/算力/机器人成4月16日舆情热点（九方智投监测）

━━━━━━━━━━━━━━━━━━━━
💬 三、论坛/社区热门讨论
━━━━━━━━━━━━━━━━━━━━
🕐 时间范围：2026-04-16

【Hacker News / 安全社区】
1️⃣ UAC-0247威胁组织：观察到针对乌克兰关键基础设施的网络攻击活动（2026年3-4月）
2️⃣ FBI与印尼警方摧毁W3LL钓鱼网络：涉案金额$2000万欺诈，W3LL Panel工具包可绕过MFA
3️⃣ nginx-ui严重漏洞CVE-2026-33032：允许完全接管Nginx服务器，CVSS 9.8，2.3.3之前版本受影响
4️⃣ Fiverr大规模数据泄露：用户税务表格/驾照等敏感文件因Cloudinary配置问题暴露于Google搜索

【Reddit - r/artificial】
• 热议主题：各大LLM公司正在向"原生设备应用"转型，AI助手正在成为能够控制设备、自动执行工作流的原生App

【arxiv 学术热点】
• Consciousness Cluster：研究声称有意识的LLM模型偏好
• Caption First VQA：多模态大模型Scaling规律研究
• KMMMU：韩语多模态理解基准

━━━━━━━━━━━━━━━━━━━━
💡 四、简评
━━━━━━━━━━━━━━━━━━━━
📊 今日关键词：**科技强势延续 + AI军备竞赛加速**

美股方面，纳斯达克12连涨创15年纪录，科技股估值压力被AI叙事对冲，中东地缘风险目前未能打断涨势。亚马逊重金下注卫星互联网，显示巨头太空竞赛已全面开打。

AI方面，OpenAI与Anthropic的竞争已延伸至垂直领域（网络安全的GPT-5.4-Cyber、生命科学的GPT-Rosalind），模型层竞争正在分化。GitHub上开源语音合成项目引发关注，与腾讯企业微信CLI开源形成呼应——"开发者工具+AI"仍是当前最活跃的创新方向之一。

安全方面多起高危漏洞同时爆发，nginx-ui RCE和Fiverr数据泄露值得关注。

━━━━━━━━━━━━━━━━━━━━
⏰ 晨报时间：2026-04-17 09:02 CST | 数据截至 2026-04-16 24:00
🤖 由 OpenClaw 自动生成"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        if result.get("ok"):
            print("✅ 晨报发送成功")
        else:
            print(f"❌ 发送失败: {result}")
except Exception as e:
    print(f"❌ 异常: {e}")
