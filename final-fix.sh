#!/bin/bash
# 修复 ETF 助手的颜色判断逻辑

SKILL_PATH="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 创建新的输出部分
cat > /tmp/new_output.txt << 'EOF'
        # 腾讯 API 返回的 change 是正数表示上涨
        local color="${NC}"
        local arrow="➡️"
        local trend="平盘"
        if [ -n "$change" ] && [ "$change" != "0.000" ] && [ "$change" != "0" ]; then
            # 使用 awk 判断正负（比 bc 更可靠）
            local sign=$(echo "$change" | awk '{if ($1 > 0) print "pos"; else if ($1 < 0) print "neg"; else print "zero"}')
            if [ "$sign" = "pos" ]; then
                color="${GREEN}"
                arrow="📈"
                trend="上涨"
            elif [ "$sign" = "neg" ]; then
                color="${RED}"
                arrow="📉"
                trend="下跌"
            fi
        fi
        echo -e "当前价格：${color}¥${current}${NC}"
        echo -e "昨收：¥${prev_close}"
        echo -e "涨跌：${color}${change} (${pct}%)${NC}"
        echo -e "${color}${arrow} ${trend}${NC}"
EOF

# 使用 sed 替换输出部分
# 找到 "echo -e "当前价格" 到 "echo -e "${RED}📉 下跌${NC}"" 并替换
sed -i '/echo -e "当前价格：\${GREEN}\$current\${NC}"/,/echo -e "\${RED}📉 下跌\${NC}"/c\        # 腾讯 API 返回的 change 是正数表示上涨\n        local color="${NC}"\n        local arrow="➡️"\n        local trend="平盘"\n        if [ -n "$change" ] \&\& [ "$change" != "0.000" ] \&\& [ "$change" != "0" ]; then\n            local sign=$(echo "$change" | awk '\''{if ($1 > 0) print "pos"; else if ($1 < 0) print "neg"; else print "zero"}'\'')\n            if [ "$sign" = "pos" ]; then\n                color="${GREEN}"\n                arrow="📈"\n                trend="上涨"\n            elif [ "$sign" = "neg" ]; then\n                color="${RED}"\n                arrow="📉"\n                trend="下跌"\n            fi\n        fi\n        echo -e "当前价格：${color}¥${current}${NC}"\n        echo -e "昨收：¥${prev_close}"\n        echo -e "涨跌：${color}${change} (${pct}%)${NC}"\n        echo -e "${color}${arrow} ${trend}${NC}"' "$SKILL_PATH"

echo "修复完成！"
