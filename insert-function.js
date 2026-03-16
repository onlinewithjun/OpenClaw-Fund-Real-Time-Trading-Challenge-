const fs = require('fs');

const skillPath = 'C:/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh';
const patchPath = 'C:/Users/Administrator/.openclaw/workspace/skills/etf-assistant/get_secid.patch';

let content = fs.readFileSync(skillPath, 'utf8');
const patch = fs.readFileSync(patchPath, 'utf8');

// 在 cmd_price() 之前插入 get_secid 函数
const insertIndex = content.indexOf('cmd_price()');
if (insertIndex === -1) {
    console.log('未找到 cmd_price 函数');
    process.exit(1);
}

const newContent = content.substring(0, insertIndex) + patch + content.substring(insertIndex);

fs.writeFileSync(skillPath, newContent, 'utf8');
console.log('get_secid 函数已插入到 cmd_price 之前');

// 现在还需要在 cmd_price 函数中添加 secid 的获取
// 找到 "local name=$(get_etf_name" 并添加 secid 获取
const nameLine = 'local name=$(get_etf_name "$code")';
const nameWithSecid = 'local name=$(get_etf_name "$code")\n    local secid=$(get_secid "$code")';

const updatedContent = newContent.replace(nameLine, nameWithSecid);
fs.writeFileSync(skillPath, updatedContent, 'utf8');
console.log('secid 变量已添加到 cmd_price 函数中');
