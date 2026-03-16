#!/bin/bash
# ETF Skill 修复脚本 - 使用腾讯 API 替换 Yahoo Finance

SKILL_PATH="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"
BACKUP_PATH="${SKILL_PATH}.bak2"

# 备份
cp "$SKILL_PATH" "$BACKUP_PATH"
echo "已备份原文件"

# 创建新的 cmd_price 函数
cat > /tmp/new_cmd_price.sh << 'EOF'
# 查询 ETF 行情 (使用腾讯 API - 临时修复)
cmd_price() {
    local code=$1
    if [ -z "$code" ]; then
        echo -e "${RED}❌ 请输入 ETF 代码${NC}"
        return 1
    fi
    
    local name=$(get_etf_name "$code")
    echo -e "${GREEN}📈 $name ($code) 实时行情${NC}"
    echo ""
    
    # 确定市场前缀
    local market="sh"
    if [[ "$code" == 15* ]] || [[ "$code" == 0* ]] || [[ "$code" == 3* ]]; then
        market="sz"
    fi
    
    # 使用腾讯 API
    local response=$(curl -s --connect-timeout 5 "http://qt.gtimg.cn/q=${market}${code}" 2>/dev/null)
    
    if echo "$response" | grep -q "v_${market}${code}="; then
        # 解析腾讯数据格式
        local data=$(echo "$response" | sed "s/v_${market}${code}=\"//" | sed 's/"$//' | sed 's/~/ /g')
        
        # 提取字段
        local current=$(echo "$data" | awk '{print $4}')
        local prev_close=$(echo "$data" | awk '{print $5}')
        local high=$(echo "$data" | awk '{print $33}')
        local low=$(echo "$data" | awk '{print $34}')
        local change=$(echo "$data" | awk '{print $32}')
        local pct=$(echo "$data" | awk '{print $31}')
        
        # 设置颜色
        local color="${NC}"
        local arrow="➡️"
        local trend="平盘"
        if [ "$change" != "" ] && [ "$change" != "0" ]; then
            if [ "$(echo "$change > 0" | bc -l 2>/dev/null)" = "1" ]; then
                color="${GREEN}"
                arrow="📈"
                trend="上涨"
            elif [ "$(echo "$change < 0" | bc -l 2>/dev/null)" = "1" ]; then
                color="${RED}"
                arrow="📉"
                trend="下跌"
            fi
        fi
        
        echo -e "当前价格：${color}¥$current${NC}"
        echo -e "昨收：¥$prev_close"
        echo -e "涨跌：${color}$change (${pct}%)${NC}"
        echo -e "最高：¥$high"
        echo -e "最低：¥$low"
        echo -e "${color}${arrow} $trend${NC}"
    else
        echo -e "${YELLOW}⚠️  暂时无法获取行情数据${NC}"
        echo "可能原因：网络问题、API 限流或 ETF 代码不存在"
    fi
}
EOF

# 添加 get_secid 函数（如果需要）
# 在 cmd_price 之前插入
awk '
/^cmd_price\(\)/ {
    system("cat /tmp/new_cmd_price.sh")
    # 跳过旧的 cmd_price 函数直到下一个函数
    while (getline && !/^# 热门 ETF/) {}
    print ""
}
{print}
' "$SKILL_PATH" > "${SKILL_PATH}.new"

mv "${SKILL_PATH}.new" "$SKILL_PATH"
echo "修改完成！"
