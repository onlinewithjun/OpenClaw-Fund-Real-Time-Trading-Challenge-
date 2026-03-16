#!/bin/bash
SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 添加编码转换到 curl 命令（使用 | 作为分隔符）
sed -i 's|curl -s "http://qt.gtimg.cn/q=${market}${code}" 2>/dev/null|curl -s "http://qt.gtimg.cn/q=${market}${code}" 2>/dev/null | iconv -f gbk -t utf-8 2>/dev/null|' "$SKILL"

echo "编码转换已添加"
