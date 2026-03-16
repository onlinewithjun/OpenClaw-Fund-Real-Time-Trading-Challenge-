#!/bin/bash
SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 1. 添加 market 变量（在 local name 之后）
sed -i '/local name=\$(get_etf_name "\$code")/a\    # 确定市场前缀\n    local market="sh"\n    if [[ "$code" == 15* ]] || [[ "$code" == 0* ]] || [[ "$code" == 3* ]]; then\n        market="sz"\n    fi' "$SKILL"

# 2. 替换 API URL
sed -i 's|https://query1.finance.yahoo.com/v8/finance/chart/|http://qt.gtimg.cn/q=|g' "$SKILL"

# 3. 替换 .SS
sed -i 's|${code}.SS"|${market}${code}"|g' "$SKILL"

# 4. 替换注释
sed -i 's|使用 Yahoo Finance API|使用腾讯 API - 临时修复|g' "$SKILL"

echo "sed 修改完成"
