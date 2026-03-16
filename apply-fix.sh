#!/bin/bash
# ETF 助手修复脚本

SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"
NEW_FUNC="/mnt/c/Users/Administrator/.openclaw/workspace/new_cmd_price.txt"

# 备份
cp "$SKILL" "${SKILL}.bak3"
echo "已备份"

# 读取新函数
NEW_CONTENT=$(cat "$NEW_FUNC")

# 使用 Python 进行替换（避免 bash 转义问题）
python3 << PYEOF
import re

with open('$SKILL', 'r', encoding='utf-8') as f:
    content = f.read()

# 读取新函数
with open('$NEW_FUNC', 'r', encoding='utf-8') as f:
    new_func = f.read()

# 找到旧函数并替换
pattern = r'# 查询 ETF 行情.*?cmd_price\(\).*?(?=# 热门 ETF)'
replacement = new_func + '\n\n'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('$SKILL', 'w', encoding='utf-8') as f:
    f.write(content)

print("替换完成")
PYEOF

echo "修复完成！"
