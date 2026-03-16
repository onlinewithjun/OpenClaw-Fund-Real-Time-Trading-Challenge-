#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成小红书封面图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建图片 (1080x1440，小红书封面比例)
width, height = 1080, 1440
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 背景渐变（从深红到浅红）
for y in range(height):
    r = int(220 + (50 * y / height))
    g = int(50 + (100 * y / height))
    b = int(50 + (100 * y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 添加标题文字
title = "AI 操盘挑战"
subtitle = "6 个月翻倍！"
money = "1000 元 → 2000 元"

# 尝试使用中文字体
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",  # 黑体
    "C:/Windows/Fonts/simkai.ttf",  # 楷体
]

title_font_size = 80
subtitle_font_size = 60
money_font_size = 50

title_font = None
subtitle_font = None
money_font = None

for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            title_font = ImageFont.truetype(font_path, title_font_size)
            subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)
            money_font = ImageFont.truetype(font_path, money_font_size)
            break
        except:
            continue

# 如果没有中文字体，使用默认字体
if title_font is None:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    money_font = ImageFont.load_default()

# 计算文字位置并绘制
# 标题
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) / 2
title_y = height * 0.25
draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)

# 副标题
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) / 2
subtitle_y = height * 0.35
draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 215, 0), font=subtitle_font)

# 金额
money_bbox = draw.textbbox((0, 0), money, font=money_font)
money_width = money_bbox[2] - money_bbox[0]
money_x = (width - money_width) / 2
money_y = height * 0.50
draw.text((money_x, money_y), money, fill=(255, 255, 255), font=money_font)

# 添加装饰元素
# 顶部装饰
draw.rectangle([(0, 0), (width, 10)], fill=(255, 215, 0))
# 底部装饰
draw.rectangle([(0, height-10), (width, height)], fill=(255, 215, 0))

# 添加 OpenClaw 标识
platform_text = "Powered by OpenClaw"
platform_font = ImageFont.load_default()
platform_bbox = draw.textbbox((0, 0), platform_text, font=platform_font)
platform_width = platform_bbox[2] - platform_bbox[0]
platform_x = (width - platform_width) / 2
platform_y = height * 0.85
draw.text((platform_x, platform_y), platform_text, fill=(255, 255, 255), font=platform_font)

# 保存
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'xhs_cover.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path, 'PNG')
print(f"封面图已保存：{output_path}")
