path = '/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换颜色判断逻辑
old_logic = '''# 获取涨跌幅颜色
        if [[ "$change" == +* ]]; then
            echo -e "${GREEN}📈 上涨${NC}"
        else
            echo -e "${RED}📉 下跌${NC}"
        fi'''

new_logic = '''# 判断涨跌方向（腾讯 API 返回的 change 不带符号）
        local color="${NC}"
        local arrow="➡️"
        local trend="平盘"
        if [ -n "$change" ] && [ "$change" != "0.000" ] && [ "$change" != "0" ]; then
            local is_up=$(echo "$change" | awk '{print ($1>0)?"1":"0"}')
            if [ "$is_up" = "1" ]; then
                color="${GREEN}"
                arrow="📈"
                trend="上涨"
            else
                color="${RED}"
                arrow="📉"
                trend="下跌"
            fi
        fi
        echo -e "${color}${arrow} ${trend}${NC}"'''

content = content.replace(old_logic, new_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("颜色判断逻辑已修复")
