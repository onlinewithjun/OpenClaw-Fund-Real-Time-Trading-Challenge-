#!/usr/bin/env python3
"""
小红书图片生成器 - 爆款风格
1080x1440 竖版，鲜艳配色，卡片式布局，醒目数据
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# 配置
IMG_WIDTH = 1080
IMG_HEIGHT = 1440

# 小红书爆款配色
COLORS = {
    'bg': '#F8F8F8',
    'card': '#FFFFFF',
    'primary': '#FF2442',    # 小红书红
    'secondary': '#FF6B81',  # 粉红
    'accent': '#FFD93D',     # 黄色
    'blue': '#4D96FF',       # 蓝色
    'green': '#6BCB77',      # 绿色
    'text': '#333333',
    'light': '#999999',
    'gradient1': '#FF2442',
    'gradient2': '#FF6B81',
}

# 字体
FONT_PATHS = {
    'bold': 'C:\\Windows\\Fonts\\simhei.ttf',
    'normal': 'C:\\Windows\\Fonts\\simsun.ttc',
}


def get_font(size, bold=False):
    """获取字体"""
    try:
        return ImageFont.truetype(FONT_PATHS['bold' if bold else 'normal'], size)
    except Exception:
        return ImageFont.load_default()


def create_base():
    """创建背景"""
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), COLORS['bg'])
    return img


def draw_card(draw, x1, y1, x2, y2, radius=20):
    """绘制卡片"""
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=COLORS['card'])
    # 添加阴影效果
    for i in range(1, 4):
        draw.rounded_rectangle([(x1-i, y1+i), (x2-i, y2+i)], radius=radius, fill=f'#000000{3-i:02X}')


def draw_gradient_header(draw, y1, y2, text, subtext=''):
    """绘制渐变头部"""
    # 渐变背景
    for y in range(y1, y2):
        ratio = (y - y1) / (y2 - y1)
        r = int(COLORS['gradient1'][1:3], 16) * (1-ratio) + int(COLORS['gradient2'][1:3], 16) * ratio
        g = int(COLORS['gradient1'][3:5], 16) * (1-ratio) + int(COLORS['gradient2'][3:5], 16) * ratio
        b = int(COLORS['gradient1'][5:7], 16) * (1-ratio) + int(COLORS['gradient2'][5:7], 16) * ratio
        draw.line([(0, y), (IMG_WIDTH, y)], fill=f'#{int(r):02X}{int(g):02X}{int(b):02X}')
    
    # 标题
    title_font = get_font(56, bold=True)
    bbox = draw.textbbox((0, 0), text, font=title_font)
    text_h = bbox[3] - bbox[1]
    title_y = y1 + (y2 - y1 - text_h) // 2
    draw.text((40, title_y), text, fill='#FFFFFF', font=title_font)


def generate_cover():
    """封面 - 爆款风格"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 渐变头部
    draw_gradient_header(draw, 0, 280, "OpenClaw", "省 Token 实战")
    
    # 主标题
    title_font = get_font(64, bold=True)
    title = "从月耗 100 万"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((IMG_WIDTH - title_w) // 2, 320), title, fill=COLORS['text'], font=title_font)
    
    # 到 20 万
    title2 = "到 20 万！"
    bbox2 = draw.textbbox((0, 0), title2, font=title_font)
    title2_w = bbox2[2] - bbox2[0]
    draw.text(((IMG_WIDTH - title2_w) // 2, 400), title2, fill=COLORS['primary'], font=title_font)
    
    # 核心数据卡片
    card_y = 520
    draw_card(draw, 80, card_y, IMG_WIDTH - 80, card_y + 280)
    
    # 大数字
    num_font = get_font(88, bold=True)
    "100 万 → 20 万"
    
    # 左边
    text1 = "100 万"
    bbox1 = draw.textbbox((0, 0), text1, font=num_font)
    w1 = bbox1[2] - bbox1[0]
    draw.text((200 - w1//2, card_y + 60), text1, fill=COLORS['light'], font=num_font)
    
    # 箭头
    arrow_font = get_font(48, bold=True)
    draw.text((IMG_WIDTH//2 - 40, card_y + 80), "↓", fill=COLORS['primary'], font=arrow_font)
    
    # 右边
    text2 = "20 万"
    bbox2 = draw.textbbox((0, 0), text2, font=num_font)
    w2 = bbox2[2] - bbox2[0]
    draw.text((IMG_WIDTH - 200 - w2//2, card_y + 60), text2, fill=COLORS['primary'], font=num_font)
    
    # 说明
    desc_font = get_font(28, bold=False)
    center_text(draw, "月 token 消耗", card_y + 180, desc_font, COLORS['text'])
    
    # 标签
    tag_font = get_font(24, bold=True)
    tags = ["节省 80%", "24 个任务", "自动运行"]
    tag_x = 120
    for tag in tags:
        # 标签背景
        tag_bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tag_w = tag_bbox[2] - tag_bbox[0] + 40
        tag_h = tag_bbox[3] - tag_bbox[1] + 20
        draw.rounded_rectangle([(tag_x, card_y + 220), (tag_x + tag_w, card_y + 220 + tag_h)], 
                              radius=10, fill=COLORS['secondary'])
        draw.text((tag_x + 20, card_y + 230), tag, fill='#FFFFFF', font=tag_font)
        tag_x += tag_w + 20
    
    # 底部 emoji
    emoji_font = get_font(32, bold=False)
    emojis = "🔥 实战分享  💡 干货满满  ⚡ 效率提升"
    bbox = draw.textbbox((0, 0), emojis, font=emoji_font)
    emoji_w = bbox[2] - bbox[0]
    draw.text(((IMG_WIDTH - emoji_w) // 2, IMG_HEIGHT - 120), emojis, fill=COLORS['light'], font=emoji_font)
    
    img.save('output/00_cover.png', 'PNG')
    print("[OK] 封面")


def center_text(draw, text, y, font, color):
    """居中绘制文本"""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((IMG_WIDTH - w) // 2, y), text, fill=color, font=font)


def generate_page1():
    """第 1 页 - 策略层"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 头部
    draw_gradient_header(draw, 0, 180, "策略层优化")
    
    # 副标题
    subtitle_font = get_font(28, bold=False)
    center_text(draw, "节省约 50% token", 200, subtitle_font, COLORS['text'])
    
    # 卡片 1
    card1_y = 260
    draw_card(draw, 60, card1_y, IMG_WIDTH - 60, card1_y + 340)
    
    # 序号
    num_font = get_font(48, bold=True)
    draw.text((80, card1_y + 20), "01", fill=COLORS['primary'], font=num_font)
    
    # 标题
    title_font = get_font(36, bold=True)
    draw.text((160, card1_y + 25), "脚本优先，AI 后置", fill=COLORS['text'], font=title_font)
    
    # 对比
    wrong_font = get_font(24, bold=False)
    draw.text((100, card1_y + 100), "❌ AI 全流程", fill=COLORS['light'], font=wrong_font)
    draw.text((100, card1_y + 135), "3000-5000 tokens", fill=COLORS['light'], font=wrong_font)
    
    right_font = get_font(28, bold=True)
    draw.text((100, card1_y + 190), "✅ 脚本计算 + AI 格式化", fill=COLORS['green'], font=right_font)
    draw.text((100, card1_y + 225), "200-500 tokens", fill=COLORS['green'], font=right_font)
    
    # 效果标签
    effect_font = get_font(22, bold=True)
    effects = [("状态刷新", "98%"), ("晚间复盘", "96%"), ("健康检查", "98%")]
    eff_y = card1_y + 290
    eff_x = 100
    for name, value in effects:
        draw.rounded_rectangle([(eff_x, eff_y), (eff_x + 140, eff_y + 40)], radius=8, fill=COLORS['blue'])
        draw.text((eff_x + 10, eff_y + 8), f"{name} {value}", fill='#FFFFFF', font=effect_font)
        eff_x += 150
    
    # 卡片 2
    card2_y = 640
    draw_card(draw, 60, card2_y, IMG_WIDTH - 60, card2_y + 220)
    
    draw.text((80, card2_y + 20), "02", fill=COLORS['primary'], font=num_font)
    draw.text((160, card2_y + 25), "模型分层，按需分配", fill=COLORS['text'], font=title_font)
    
    # 模型分配
    model_font = get_font(24, bold=False)
    draw.text((100, card2_y + 90), "95% 任务", fill=COLORS['text'], font=model_font)
    draw.text((250, card2_y + 90), "qwen3.5-plus", fill=COLORS['blue'], font=get_font(24, bold=True))
    
    draw.text((100, card2_y + 130), "5% 关键任务", fill=COLORS['text'], font=model_font)
    draw.text((280, card2_y + 130), "gpt-5.4", fill=COLORS['primary'], font=get_font(24, bold=True))
    
    # 页码
    page_font = get_font(20, bold=True)
    draw.text((IMG_WIDTH - 80, IMG_HEIGHT - 50), "1 / 5", fill=COLORS['light'], font=page_font)
    
    img.save('output/01_strategy.png', 'PNG')
    print("[OK] 第 1 页")


def generate_page2():
    """第 2 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    draw_gradient_header(draw, 0, 180, "策略层优化（续）")
    
    # 卡片 3
    card_y = 220
    draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 240)
    
    num_font = get_font(48, bold=True)
    draw.text((80, card_y + 20), "03", fill=COLORS['primary'], font=num_font)
    
    title_font = get_font(36, bold=True)
    draw.text((160, card_y + 25), "会话隔离", fill=COLORS['text'], font=title_font)
    
    text_font = get_font(24, bold=False)
    draw.text((100, card_y + 90), "日常任务：main + systemEvent", fill=COLORS['text'], font=text_font)
    draw.text((100, card_y + 130), "资讯/复盘：isolated + agentTurn", fill=COLORS['blue'], font=get_font(24, bold=True))
    
    result_font = get_font(28, bold=True)
    draw.text((100, card_y + 180), "主会话上下文 < 20%", fill=COLORS['green'], font=result_font)
    
    # 卡片 4
    card_y = 500
    draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 240)
    
    draw.text((80, card_y + 20), "04", fill=COLORS['primary'], font=num_font)
    draw.text((160, card_y + 25), "静默成功，失败才报警", fill=COLORS['text'], font=title_font)
    
    draw.text((100, card_y + 90), "健康时不推送", fill=COLORS['light'], font=text_font)
    draw.text((100, card_y + 130), "失败才告警", fill=COLORS['primary'], font=get_font(24, bold=True))
    
    draw.text((100, card_y + 180), "日均 24 条 → 2-5 条（省 85%）", fill=COLORS['green'], font=result_font)
    
    # 卡片 5
    card_y = 780
    draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 280)
    
    draw.text((80, card_y + 20), "05", fill=COLORS['primary'], font=num_font)
    draw.text((160, card_y + 25), "决策短输出", fill=COLORS['text'], font=title_font)
    
    # 代码块
    code_font = get_font(20, bold=False)
    code_bg = '#F5F5F5'
    code_text = "[BUY] 020899 72CNY | gate_consensus | before 15:00"
    draw.rounded_rectangle([(100, card_y + 90), (IMG_WIDTH - 100, card_y + 150)], radius=8, fill=code_bg)
    center_text(draw, code_text, card_y + 105, code_font, COLORS['text'])
    
    draw.text((100, card_y + 180), "50 tokens（vs 2000 tokens）", fill=COLORS['green'], font=result_font)
    draw.text((100, card_y + 220), "节省 97.5%！", fill=COLORS['primary'], font=get_font(28, bold=True))
    
    # 页码
    page_font = get_font(20, bold=True)
    draw.text((IMG_WIDTH - 80, IMG_HEIGHT - 50), "2 / 5", fill=COLORS['light'], font=page_font)
    
    img.save('output/02_strategy2.png', 'PNG')
    print("[OK] 第 2 页")


def generate_page3():
    """第 3 页 - 工具层"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    draw_gradient_header(draw, 0, 180, "工具层优化")
    
    subtitle_font = get_font(28, bold=False)
    center_text(draw, "节省约 30% token", 200, subtitle_font, COLORS['text'])
    
    # 卡片 6
    card_y = 260
    draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 320)
    
    num_font = get_font(48, bold=True)
    draw.text((80, card_y + 20), "06", fill=COLORS['primary'], font=num_font)
    
    title_font = get_font(36, bold=True)
    draw.text((160, card_y + 25), "Tavily 搜索", fill=COLORS['text'], font=title_font)
    
    # 对比图
    draw.rounded_rectangle([(100, card_y + 90), (480, card_y + 200)], radius=12, fill='#FFEBEE')
    draw.text((120, card_y + 110), "传统搜索", fill=COLORS['light'], font=get_font(24, bold=False))
    draw.text((120, card_y + 150), "5000+ tokens", fill=COLORS['light'], font=get_font(32, bold=True))
    
    draw.rounded_rectangle([(560, card_y + 90), (940, card_y + 200)], radius=12, fill='#E8F5E9')
    draw.text((580, card_y + 110), "Tavily", fill=COLORS['green'], font=get_font(24, bold=True))
    draw.text((580, card_y + 150), "800 tokens", fill=COLORS['green'], font=get_font(32, bold=True))
    
    draw.text((IMG_WIDTH//2 - 80, card_y + 240), "节省 84%", fill=COLORS['primary'], font=get_font(36, bold=True))
    
    # 卡片 7
    card_y = 620
    draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 320)
    
    draw.text((80, card_y + 20), "07", fill=COLORS['primary'], font=num_font)
    draw.text((160, card_y + 25), "QMD Memory 检索", fill=COLORS['text'], font=title_font)
    
    draw.text((100, card_y + 90), "本地 SQLite + BM25 + 向量检索", fill=COLORS['light'], font=get_font(24, bold=False))
    
    # 对比
    draw.rounded_rectangle([(100, card_y + 140), (480, card_y + 230)], radius=12, fill='#FFEBEE')
    draw.text((120, card_y + 165), "传统检索", fill=COLORS['light'], font=get_font(24, bold=False))
    draw.text((120, card_y + 195), "5000 tokens", fill=COLORS['light'], font=get_font(32, bold=True))
    
    draw.rounded_rectangle([(560, card_y + 140), (940, card_y + 230)], radius=12, fill='#E3F2FD')
    draw.text((580, card_y + 165), "QMD", fill=COLORS['blue'], font=get_font(24, bold=True))
    draw.text((580, card_y + 195), "300 tokens", fill=COLORS['blue'], font=get_font(32, bold=True))
    
    draw.text((IMG_WIDTH//2 - 80, card_y + 270), "节省 94%", fill=COLORS['primary'], font=get_font(36, bold=True))
    
    # 页码
    page_font = get_font(20, bold=True)
    draw.text((IMG_WIDTH - 80, IMG_HEIGHT - 50), "3 / 5", fill=COLORS['light'], font=page_font)
    
    img.save('output/03_tools.png', 'PNG')
    print("[OK] 第 3 页")


def generate_page4():
    """第 4 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    draw_gradient_header(draw, 0, 180, "工具层优化（续）")
    
    # 卡片 8-10
    cards = [
        ("08", "文本摘要技能", "长文压缩 90%", COLORS['accent'], '#FFF9E6'),
        ("09", "本地缓存 + 证据压缩", "JSON 压缩 80%+", COLORS['blue'], '#E3F2FD'),
        ("10", "Memory 分级 + 归档", "检索 token 降 60%", COLORS['green'], '#E8F5E9'),
    ]
    
    for i, (num, title, desc, color, bg) in enumerate(cards):
        card_y = 220 + i * 260
        draw_card(draw, 60, card_y, IMG_WIDTH - 60, card_y + 220)
        
        num_font = get_font(48, bold=True)
        draw.text((80, card_y + 20), num, fill=color, font=num_font)
        
        title_font = get_font(32, bold=True)
        draw.text((160, card_y + 25), title, fill=COLORS['text'], font=title_font)
        
        desc_font = get_font(28, bold=True)
        draw.text((100, card_y + 100), desc, fill=color, font=desc_font)
        
        # 小字说明
        if i == 1:
            text_font = get_font(22, bold=False)
            draw.text((100, card_y + 150), "金融数据 5-15 分钟  •  新闻 1-4 小时", fill=COLORS['light'], font=text_font)
        elif i == 2:
            text_font = get_font(22, bold=False)
            draw.text((100, card_y + 150), "三层结构：长期 + 日常 + 归档", fill=COLORS['light'], font=text_font)
            draw.text((100, card_y + 180), "检索命中率 80%+", fill=COLORS['green'], font=get_font(24, bold=True))
    
    # 页码
    page_font = get_font(20, bold=True)
    draw.text((IMG_WIDTH - 80, IMG_HEIGHT - 50), "4 / 5", fill=COLORS['light'], font=page_font)
    
    img.save('output/04_tools2.png', 'PNG')
    print("[OK] 第 4 页")


def generate_page5():
    """第 5 页 - 总结"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    draw_gradient_header(draw, 0, 220, "总体效果")
    
    # 大卡片
    card_y = 260
    draw_card(draw, 40, card_y, IMG_WIDTH - 40, card_y + 520)
    
    # 效果对比
    effects = [
        ("月 token", "100 万", "20 万", "80%", COLORS['primary']),
        ("主上下文", "80%+", "20%", "75%", COLORS['blue']),
        ("日均推送", "24 条", "2-5 条", "85%", COLORS['green']),
        ("强模型", "50%", "5%", "90%", COLORS['accent']),
    ]
    
    result_font = get_font(32, bold=True)
    label_font = get_font(24, bold=False)
    
    for i, (label, before, after, saving, color) in enumerate(effects):
        y = card_y + 40 + i * 120
        
        # 标签
        draw.text((80, y + 10), label, fill=COLORS['light'], font=label_font)
        
        # 之前
        draw.text((80, y + 50), before, fill=COLORS['light'], font=get_font(28, bold=True))
        
        # 箭头
        draw.text((280, y + 50), "→", fill=COLORS['light'], font=get_font(28, bold=True))
        
        # 之后
        draw.text((340, y + 50), after, fill=color, font=result_font)
        
        # 节省
        draw.text((IMG_WIDTH - 180, y + 50), saving, fill=color, font=get_font(36, bold=True))
        
        # 分隔线
        if i < 3:
            draw.line([(80, y + 110), (IMG_WIDTH - 80, y + 110)], fill='#EEEEEE', width=2)
    
    # 金句卡片
    quote_y = 820
    draw_card(draw, 60, quote_y, IMG_WIDTH - 60, quote_y + 180)
    draw.text((100, quote_y + 40), "💡 省 token 不是为了抠门", fill=COLORS['text'], font=get_font(28, bold=False))
    draw.text((100, quote_y + 90), "是为了让系统更可持续", fill=COLORS['primary'], font=get_font(32, bold=True))
    
    # 标签
    tag_font = get_font(20, bold=True)
    tags = "#OpenClaw  #AI 自动化  #token 优化  #效率工具"
    center_text(draw, tags, IMG_HEIGHT - 80, tag_font, COLORS['light'])
    
    # 页码
    page_font = get_font(20, bold=True)
    draw.text((IMG_WIDTH - 80, IMG_HEIGHT - 50), "5 / 5", fill=COLORS['light'], font=page_font)
    
    img.save('output/05_summary.png', 'PNG')
    print("[OK] 第 5 页")


def main():
    """主函数"""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("生成小红书爆款风格图片...")
    print("=" * 40)
    
    generate_cover()
    generate_page1()
    generate_page2()
    generate_page3()
    generate_page4()
    generate_page5()
    
    print("=" * 40)
    print("完成！6 张图片已保存到 output/")


if __name__ == '__main__':
    main()
