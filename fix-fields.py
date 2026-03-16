path = '/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修正字段编号（因为有空字段导致偏移）
content = content.replace("cut -d'~' -f31", "cut -d'~' -f32")
content = content.replace("cut -d'~' -f32", "cut -d'~' -f33")

# 但是上面的替换会把 f31->f32 然后 f32->f33，需要重新处理
# 重新读取
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 正确替换
content = content.replace("local change=$(echo \"$data\" | cut -d'~' -f31)", "local change=$(echo \"$data\" | cut -d'~' -f32)")
content = content.replace("local pct=$(echo \"$data\" | cut -d'~' -f32)", "local pct=$(echo \"$data\" | cut -d'~' -f33)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("字段编号已修正为 f32 和 f33")
