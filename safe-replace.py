import re

skill_path = r'C:\Users\Administrator\.openclaw\workspace\skills\etf-assistant\etf-assistant.sh'
new_func_path = r'C:\Users\Administrator\.openclaw\workspace\new_cmd_price.txt'

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

with open(new_func_path, 'r', encoding='utf-8') as f:
    new_func = f.read()

# 找到 cmd_price 函数的开始和结束
# 开始：cmd_price() {
# 结束：下一个函数定义（以 # 开头的注释行，后跟函数名()）

start_marker = 'cmd_price()'
end_markers = ['# 热门 ETF', '# 搜索 ETF']

start = content.find(start_marker)
if start == -1:
    print("未找到 cmd_price")
    exit(1)

# 找到函数体结束（下一个 # 开头的行）
end = len(content)
for marker in end_markers:
    pos = content.find(marker, start)
    if pos != -1 and pos < end:
        end = pos
        break

# 替换
new_content = content[:start] + new_func + content[end:]

with open(skill_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"替换成功！从位置 {start} 到 {end}")
print(f"新文件长度：{len(new_content)}")
