path = '/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 添加 iconv 转换
old = 'curl -s "http://qt.gtimg.cn/q=${market}${code}" 2>/dev/null | head -100'
new = 'curl -s "http://qt.gtimg.cn/q=${market}${code}" 2>/dev/null | iconv -f gbk -t utf-8 2>/dev/null | head -100'

content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("编码转换已添加")
