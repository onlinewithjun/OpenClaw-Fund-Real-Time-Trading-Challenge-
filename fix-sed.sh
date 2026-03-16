#!/bin/bash
SKILL="/mnt/c/Users/Administrator/.openclaw/workspace/skills/etf-assistant/etf-assistant.sh"

# 替换 sed 解析逻辑 - 使用更简单的方法
sed -i "s|sed 's/.*=\"//'|sed 's/^[^\"]*\"//'|" "$SKILL"
sed -i "s|sed 's/\".*//'|sed 's/\".*\$//'|" "$SKILL"

echo "sed 解析已修复"
