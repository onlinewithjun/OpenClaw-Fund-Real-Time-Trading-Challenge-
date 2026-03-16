const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh';

let content = fs.readFileSync(path, 'utf8');

// 1. 替换注释
content = content.replace(
    '# 查询 ETF 行情 (使用 Yahoo Finance API)',
    '# 查询 ETF 行情 (使用腾讯 API - 临时修复)'
);

// 2. 添加 market 变量 - 使用 \\${} 转义
const marketAdd = 'local name=$(get_etf_name "$code")\n    # 确定市场前缀\n    local market="sh"\n    if [[ "$code" == 15* ]] || [[ "$code" == 0* ]] || [[ "$code" == 3* ]]; then\n        market="sz"\n    fi\n    echo -e "${GREEN}📈 $name ($code) 实时行情${NC}"';

content = content.replace(
    'local name=$(get_etf_name "$code")\n    echo -e "${GREEN}📈 $name ($code) 实时行情${NC}"',
    marketAdd
);

// 3. 替换 API URL
content = content.replace(
    'https://query1.finance.yahoo.com/v8/finance/chart/${code}.SS',
    'http://qt.gtimg.cn/q=${market}${code}'
);

// 4. 替换条件判断
content = content.replace(
    'if echo "$response" | grep -q "timestamp"; then',
    'if echo "$response" | grep -q "v_${market}${code}="; then'
);

// 5. 替换整个数据解析和输出部分
const oldParse = '# 提取价格数据\n        local current=$(echo "$response" | python3 -c "\nimport json, sys\ntry:\n    data = json.load(sys.stdin)\n    result = data.get(\'chart\', {}).get(\'result\', [{}])[0]\n    meta = result.get(\'meta\', {})\n    print(meta.get(\'regularMarketPrice\', \'N/A\'))\nexcept: print(\'N/A\')\n" 2>/dev/null)\n        \n        local prev_close=$(echo "$response" | python3 -c "\nimport json, sys\ntry:\n    data = json.load(sys.stdin)\n    result = data.get(\'chart\', {}).get(\'result\', [{}])[0]\n    meta = result.get(\'meta\', {})\n    print(meta.get(\'previousClose\', \'N/A\'))\nexcept: print(\'N/A\')\n" 2>/dev/null)\n        \n        local change=$(echo "$response" | python3 -c "\nimport json, sys\ntry:\n    data = json.load(sys.stdin)\n    result = data.get(\'chart\', {}).get(\'result\', [{}])[0]\n    meta = result.get(\'meta\', {})\n    diff = float(meta.get(\'regularMarketPrice\', 0)) - float(meta.get(\'previousClose\', 0))\n    pct = diff / float(meta.get(\'previousClose\', 1)) * 100\n    print(f\'{diff:+.4f} ({pct:+.2f}%)\')\nexcept: print(\'N/A\')\n" 2>/dev/null)\n        \n        echo -e "当前价格：${GREEN}$current${NC}"\n        echo -e "昨收：$prev_close"\n        echo -e "涨跌：$change"\n        \n        # 获取涨跌幅颜色\n        if [[ "$change" == +* ]]; then\n            echo -e "${GREEN}📈 上涨${NC}"\n        else\n            echo -e "${RED}📉 下跌${NC}"\n        fi';

const newParse = '# 解析腾讯数据格式\n        local data=$(echo "$response" | sed \'s/.*="//\' | sed \'s/".*//\')\n        local current=$(echo "$data" | cut -d\'~\' -f4)\n        local prev_close=$(echo "$data" | cut -d\'~\' -f5)\n        local change=$(echo "$data" | cut -d\'~\' -f31)\n        local pct=$(echo "$data" | cut -d\'~\' -f32)\n        \n        # 判断涨跌方向\n        local color="${NC}"\n        local arrow="➡️"\n        local trend="平盘"\n        if [ -n "$change" ] && [ "$change" != "0.000" ] && [ "$change" != "0" ]; then\n            local is_up=$(echo "$change" | awk \'{print ($1>0)?"1":"0"}\')\n            if [ "$is_up" = "1" ]; then\n                color="${GREEN}"\n                arrow="📈"\n                trend="上涨"\n            else\n                color="${RED}"\n                arrow="📉"\n                trend="下跌"\n            fi\n        fi\n        \n        echo -e "当前价格：${color}¥${current}${NC}"\n        echo -e "昨收：¥${prev_close}"\n        echo -e "涨跌：${color}${change} (${pct}%)${NC}"\n        echo -e "${color}${arrow} ${trend}${NC}"';

content = content.replace(oldParse, newParse);

fs.writeFileSync(path, content, 'utf8');
console.log('修复完成！');
