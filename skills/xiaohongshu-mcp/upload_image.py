#!/usr/bin/env python3
"""Test publish to Xiaohongshu."""
import requests
import json

BASE_URL = "http://localhost:18060"

payload = {
    "title": "AI 助手调教成架构师 + 量化师",
    "content": "⚡ 今天花了一下午配置 OpenClaw，效果惊艳到我了！🎯 人设定制：OpenHarmony 架构师 + 量化策略师 + 小红书运营。🛠️ 技能安装：alphaear 金融套件 (9 个)、小红书 MCP、apipick 企业百科。📊 实测效果：OpenHarmony 笔记 22 条秒出、A 股实时数据。💡 最惊喜：数据真实性原则！⚠️ 小插曲：Defender 误报、速率限制。🎁 配置清单评论区见～ #OpenClaw #AI 助手 #量化交易 #OpenHarmony",
    "images": ["https://files.catbox.moe/y289h5.png"]
}

try:
    resp = requests.post(f"{BASE_URL}/api/v1/publish", json=payload, timeout=120)
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
