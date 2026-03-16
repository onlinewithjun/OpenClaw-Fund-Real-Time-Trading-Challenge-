#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成小红书技能列表配图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建图片 (1080x1440，小红书封面比例)
width, height = 1080, 1440
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 背景（浅蓝色）
for y in range(height):
    r = int(240 + (10 * y / height))
    g = int(245 + (5 * y / height))
    b = int(255 - (10 * y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 标题
title = "AI 的金融技能装备"
title_font_size = 60

# 技能分类
skills = [
    ("📰 新闻资讯类", [
        "alphaear-news - 实时金融新闻",
        "alphaear-search - 金融专业搜索"
    ]),
    ("📊 数据分析类", [
        "alphaear-deepear-lite - 深度市场洞察",
        "alphaear-sentiment - 市场情绪分析",
        "alphaear-signal-tracker - 信号追踪"
    ]),
    ("📈 股票基金类", [
        "alphaear-stock - A 股/港股/美股数据",
        "etf-assistant - ETF 投资助理",
        "akshare-skill - 中国金融数据"
    ]),
    ("🔮 预测分析类", [
        "alphaear-predictor - 市场预测",
        "alphaear-reporter - 金融报告生成",
        "alphaear-logic-visualizer - 逻辑可视化"
    ]),
    ("📉 研究类", [
        "research-cog - 深度研究代理",
        "charts - 数据图表生成"
    ])
]

# 尝试使用中文字体
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",  # 黑体
    "C:/Windows/Fonts/simkai.ttf",  # 楷体
]

title_font = None
category_font = None
skill_font = None

for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            title_font = ImageFont.truetype(font_path, title_font_size)
            category_font = ImageFont.truetype(font_path, 35)
            skill_font = ImageFont.truetype(font_path, 28)
            break
        except:
            continue

# 如果没有中文字体，使用默认字体
if title_font is None:
    title_font = ImageFont.load_default()
    category_font = ImageFont.load_default()
    skill_font = ImageFont.load_default()

# 绘制标题
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) / 2
title_y = 50
draw.text((title_x, title_y), title, fill=(50, 50, 150), font=title_font)

# 绘制技能列表
current_y = 150
margin = 50

for category_name, skill_list in skills:
    # 分类标题（带 emoji）
    draw.text((margin, current_y), category_name, fill=(100, 100, 180), font=category_font)
    current_y += 45
    
    # 技能列表
    for skill in skill_list:
        draw.text((margin + 20, current_y), "• " + skill, fill=(80, 80, 120), font=skill_font)
        current_y += 35
    
    current_y += 20  # 分类间距

# 底部说明
footer_text = "所有技能通过 OpenClaw 平台调用"
footer_font = ImageFont.load_default()
footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
footer_width = footer_bbox[2] - footer_bbox[0]
footer_x = (width - footer_width) / 2
footer_y = height - 50
draw.text((footer_x, footer_y), footer_text, fill=(100, 100, 100), font=footer_font)

# 保存
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'xhs_skills.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path, 'PNG')
print(f"技能列表图已保存：{output_path}")
