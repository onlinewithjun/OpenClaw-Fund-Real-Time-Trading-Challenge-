import re

skill_path = r'C:\Users\Administrator\.openclaw\workspace\skills\etf-assistant\etf-assistant.sh'
new_func_path = r'C:\Users\Administrator\.openclaw\workspace\new_cmd_price.txt'

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(new_func_path, 'r', encoding='utf-8') as f:
    new_func = f.read()

# 找到 cmd_price 函数并替换
# 从 "cmd_price()" 开始到下一个函数 "# 热门" 之前
start = content.find('cmd_price()')
if start == -1:
    print("未找到 cmd_price 函数")
    exit(1)

# 找到下一个函数的开始
end_markers = ['# 热门 ETF', '# 搜索 ETF', '# ETF 对比']
end = len(content)
for marker in end_markers:
    pos = content.find(marker, start)
    if pos != -1 and pos < end:
        end = pos

# 替换
new_content = content[:start] + new_func + '\n' + content[end:]

with open(skill_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("替换成功！")
