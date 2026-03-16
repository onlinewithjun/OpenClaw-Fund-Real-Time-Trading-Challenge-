#!/bin/bash
SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 替换条件判断
sed -i 's/grep -q "timestamp"/grep -q "v_${market}${code}="/' "$SKILL"

# 替换数据解析 - 使用 Python（WSL 路径）
python3 << 'PYEOF'
path = '/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换数据解析部分
old_parse = '''if echo "$response" | grep -q "v_${market}${code}="; then
        # 提取价格数据
        local current=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    result = data.get('chart', {}).get('result', [{}])[0]
    meta = result.get('meta', {})
    print(meta.get('regularMarketPrice', 'N/A'))
except: print('N/A')
" 2>/dev/null)
        
        local prev_close=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    result = data.get('chart', {}).get('result', [{}])[0]
    meta = result.get('meta', {})
    print(meta.get('previousClose', 'N/A'))
except: print('N/A')
" 2>/dev/null)
        
        local change=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    result = data.get('chart', {}).get('result', [{}])[0]
    meta = result.get('meta', {})
    diff = float(meta.get('regularMarketPrice', 0)) - float(meta.get('previousClose', 0))
    pct = diff / float(meta.get('previousClose', 1)) * 100
    print(f'{diff:+.4f} ({pct:+.2f}%)')
except: print('N/A')
" 2>/dev/null)'''

new_parse = '''if echo "$response" | grep -q "v_${market}${code}="; then
        # 解析腾讯数据格式
        local data=$(echo "$response" | sed 's/.*="//' | sed 's/".*//')
        local current=$(echo "$data" | cut -d'~' -f4)
        local prev_close=$(echo "$data" | cut -d'~' -f5)
        local change=$(echo "$data" | cut -d'~' -f31)
        local pct=$(echo "$data" | cut -d'~' -f32)'''

content = content.replace(old_parse, new_parse)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("解析逻辑已替换")
PYEOF

echo "修复完成"
