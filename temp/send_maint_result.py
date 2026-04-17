# -*- coding: utf-8 -*-
import json
import ssl
import urllib.request

TOKEN = "[REDACTED - Telegram bot token - REQUIRES ROTATION]"
CHAT_ID = "7107266459"

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

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = json.dumps({
    "chat_id": CHAT_ID,
    "text": msg,
    "parse_mode": "HTML"
}).encode("utf-8")

req = urllib.request.Request(url, data=data, headers={
    "Content-Type": "application/json"
})

try:
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("SEND_OK:", result.get("ok"), "msg_id:", result.get("result", {}).get("message_id"))
except Exception as e:
    print("SEND_ERROR:", e)
