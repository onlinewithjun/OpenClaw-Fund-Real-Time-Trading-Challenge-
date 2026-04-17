# -*- coding: utf-8 -*-
import json
import ssl
import urllib.request

token = "8711552917:AAE_ZcauiZ0RNX98K_XIs22gbGi0ZoHNIyY"
chat_id = "7107266459"

msg = """🧹 基金挑战#16 维护清理完成 (22:05)

✅ 缓存已清理: 0个 (已为空)
✅ 输出目录: 0个已删除
✅ 运行时快照: 0个已删除
✅ 遗留文件: 0个已删除
✅ 证据存档: 5个已归档
✅ PyCache: 1个目录已删除

所有维护任务完成，workspace 整洁。"""

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

data = json.dumps({"chat_id": chat_id, "text": msg}).encode("utf-8")
req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        print("OK:", r.read().decode())
except Exception as e:
    print("ERROR:", e)
