#!/usr/bin/env python3
import os, json, urllib.request

for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']:
    os.environ.pop(k, None)

token = "8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY"
data = json.dumps({"chat_id": "7107266459", "text": "晨报测试 - 此bot可用"}).encode("utf-8")
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
