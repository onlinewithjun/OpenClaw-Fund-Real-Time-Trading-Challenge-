const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh';

let content = fs.readFileSync(path, 'utf8');

// 替换输出部分
const oldOutput = 'echo -e "当前价格：${GREEN}$current${NC}"\n        echo -e "昨收：$prev_close"\n        echo -e "涨跌：$change"\n        \n        # 获取涨跌幅颜色\n        if [[ "$change" == +* ]]; then\n            echo -e "${GREEN}📈 上涨${NC}"\n        else\n            echo -e "${RED}📉 下跌${NC}"\n        fi';

const newOutput = `local color="${NC}"
        local arrow="➡️"
        local trend="平盘"
        # 腾讯 API 返回的 change 不带符号，需要判断
        if [ -n "$change" ] && [ "$change" != "0.000" ] && [ "$change" != "0" ]; then
            local check=$(echo "$change > 0" | bc -l 2>/dev/null)
            if [ "$check" = "1" ]; then
                color="${GREEN}"
                arrow="📈"
                trend="上涨"
            else
                check=$(echo "$change < 0" | bc -l 2>/dev/null)
                if [ "$check" = "1" ]; then
                    color="${RED}"
                    arrow="📉"
                    trend="下跌"
                fi
            fi
        fi
        echo -e "当前价格：${color}¥${current}${NC}"
        echo -e "昨收：¥${prev_close}"
        echo -e "涨跌：${color}${change} (${pct}%)${NC}"
        echo -e "${color}${arrow} ${trend}${NC}"`;

content = content.replace(oldOutput, newOutput);

fs.writeFileSync(path, content, 'utf8');
console.log('输出格式已修复！');
