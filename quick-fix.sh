#!/bin/bash
SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 1. 交换 change 和 pct 的字段（31 是涨跌额，32 是涨跌幅%）
sed -i "s/local change=\$(echo \"\$data\" | cut -d'~' -f32)/local change=\$(echo \"\$data\" | cut -d'~' -f31)/" "$SKILL"
sed -i "s/local pct=\$(echo \"\$data\" | cut -d'~' -f31)/local pct=\$(echo \"\$data\" | cut -d'~' -f32)/" "$SKILL"

# 2. 替换颜色判断逻辑
sed -i '/# 获取涨跌幅颜色/,/echo -e "\${RED}📉 下跌\${NC}"/c\        # 判断涨跌方向\n        local color="${NC}"\n        local arrow="➡️"\n        local trend="平盘"\n        if [ -n "$change" ] \&\& [ "$change" != "0.000" ]; then\n            if [ $(echo "$change" | awk '\''{print ($1>0)?"1":"0"}'\'') = "1" ]; then\n                color="${GREEN}"; arrow="📈"; trend="上涨"\n            else\n                color="${RED}"; arrow="📉"; trend="下跌"\n            fi\n        fi\n        echo -e "当前价格：${color}¥${current}${NC}"\n        echo -e "昨收：¥${prev_close}"\n        echo -e "涨跌：${color}${change} (${pct}%)${NC}"\n        echo -e "${color}${arrow} ${trend}${NC}"' "$SKILL"

echo "修复完成！"
