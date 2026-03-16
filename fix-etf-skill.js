const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh';

let content = fs.readFileSync(path, 'utf8');

// 添加 get_secid 函数（在 cmd_price 之前）
const getSecidFunc = `
# 获取 ETF 市场代码（东方财富 API）
# 上海证券交易所：1.xxxxxx (51xxxx)
# 深圳证券交易所：0.xxxxxx (15xxxx/0xxxxx)
get_secid() {
    local code=$1
    if [[ "$code" == 51* ]] || [[ "$code" == 60* ]]; then
        echo "1.${code}"
    else
        echo "0.${code}"
    fi
}
`;

// 替换 cmd_price 函数的注释
content = content.replace(
    '# 查询 ETF 行情 (使用 Yahoo Finance API)',
    '# 查询 ETF 行情 (使用东方财富 API - 临时修复)'
);

// 替换 API URL
content = content.replace(
    'https://query1.finance.yahoo.com/v8/finance/chart/${code}.SS',
    'https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f44,f45,f46,f47,f48,f106,f107"'
);

// 在 cmd_price 函数中添加 secid 获取
content = content.replace(
    'local name=$(get_etf_name "$code")\n    echo -e "${GREEN}📈 $name ($code) 实时行情${NC}"',
    'local name=$(get_etf_name "$code")\n    local secid=$(get_secid "$code")\n    echo -e "${GREEN}📈 $name ($code) 实时行情${NC}"'
);

// 在 cmd_price 函数开头添加 secid 变量声明
const oldPriceFunc = 'cmd_price() {\n    local code=$1';
const newPriceFunc = 'cmd_price() {\n    local code=$1\n    local secid=""';
content = content.replace(oldPriceFunc, newPriceFunc);

// 添加调试输出
const debugLine = 'echo "DEBUG: secid=$secid" >&2\n    ';
content = content.replace(
    'local response=$(curl -s "https://push2.eastmoney.com',
    'local response=$(curl -s "https://push2.eastmoney.com'
);

fs.writeFileSync(path, content, 'utf8');
console.log('文件修改完成！');
console.log('注意：这只是临时修复，可能需要手动调整 cmd_price 函数的数据解析逻辑');
