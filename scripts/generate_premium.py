#!/usr/bin/env python3
"""
小红书图片生成器 - 高级极简风格
参考：Apple、Muji、高端杂志排版
核心：留白、层次、克制
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

IMG_WIDTH = 1080
IMG_HEIGHT = 1440

# 高级配色 - 克制
COLORS = {
    'bg': '#FAFAFA',       # 暖白
    'card': '#FFFFFF',
    'text': '#111111',     # 深黑
    'secondary': '#666666', # 中灰
    'light': '#999999',    # 浅灰
    'accent': '#E74C3C',   # 点缀红（克制使用）
    'line': '#E5E5E5',
}

# 间距系统
SPACE = {
    'xs': 8,
    'sm': 16,
    'md': 24,
    'lg': 40,
    'xl': 64,
    'xxl': 96,
}

# 字体层级
TYPE = {
    'display': 72,
    'h1': 48,
    'h2': 36,
    'h3': 28,
    'body': 22,
    'caption': 18,
    'tiny': 14,
}

FONT_PATHS = {
    'bold': 'C:\\Windows\\Fonts\\simhei.ttf',
    'normal': 'C:\\Windows\\Fonts\\simsun.ttc',
}

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATHS['bold' if bold else 'normal'], size)
    except:
        return ImageFont.load_default()

def create_base():
    return Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), COLORS['bg'])

def center_x(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return (IMG_WIDTH - (bbox[2] - bbox[0])) // 2

def draw_line(draw, y, x1=None, x2=None, color=None):
    x1 = x1 or SPACE['xl']
    x2 = x2 or IMG_WIDTH - SPACE['xl']
    draw.line([(x1, y), (x2, y)], fill=color or COLORS['line'], width=1)

def generate_cover():
    """封面 - 极致简约"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 顶部标签 - 克制
    tag_font = get_font(TYPE['tiny'], False)
    tag = "OpenClaw 实战分享"
    draw.text((SPACE['xl'], SPACE['xl']), tag, fill=COLORS['light'], font=tag_font)
    
    # 主标题 - 大但不过分
    title_font = get_font(TYPE['display'], True)
    title = "OpenClaw"
    x = center_x(draw, title, title_font)
    draw.text((x, 280), title, fill=COLORS['text'], font=title_font)
    
    # 副标题
    subtitle_font = get_font(TYPE['h2'], False)
    subtitle = "省 Token 实战"
    x = center_x(draw, subtitle, subtitle_font)
    draw.text((x, 380), subtitle, fill=COLORS['secondary'], font=subtitle_font)
    
    # 分隔线 - 细
    draw_line(draw, 460)
    
    # 核心数据 - 聚焦
    data_y = 540
    
    # 100 万
    big_font = get_font(88, True)
    text1 = "100 万"
    bbox1 = draw.textbbox((0, 0), text1, font=big_font)
    w1 = bbox1[2] - bbox1[0]
    draw.text((IMG_WIDTH//2 - 150 - w1//2, data_y), text1, fill=COLORS['light'], font=big_font)
    
    # 箭头
    arrow_font = get_font(36, False)
    draw.text((IMG_WIDTH//2 - 25, data_y + 20), "→", fill=COLORS['light'], font=arrow_font)
    
    # 20 万 - 强调
    text2 = "20 万"
    bbox2 = draw.textbbox((0, 0), text2, font=big_font)
    w2 = bbox2[2] - bbox2[0]
    draw.text((IMG_WIDTH//2 + 150 - w2//2, data_y), text2, fill=COLORS['accent'], font=big_font)
    
    # 说明
    desc_font = get_font(TYPE['body'], False)
    desc = "月 token 消耗"
    x = center_x(draw, desc, desc_font)
    draw.text((x, data_y + 110), desc, fill=COLORS['secondary'], font=desc_font)
    
    # 数据标签 - 水平排列
    tag_font = get_font(TYPE['caption'], False)
    tags = ["节省 80%", "24 个定时任务", "每日自动运行"]
    tag_y = data_y + 170
    total_w = sum([draw.textbbox((0, 0), t, font=tag_font)[2] for t in tags]) + SPACE['md'] * (len(tags)-1)
    tag_x = (IMG_WIDTH - total_w) // 2
    
    for tag in tags:
        draw.text((tag_x, tag_y), tag, fill=COLORS['secondary'], font=tag_font)
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tag_x += bbox[2] - bbox[0] + SPACE['md']
    
    # 底部 - 极简书名号风格
    bottom_y = IMG_HEIGHT - SPACE['xxl']
    draw_line(draw, bottom_y - SPACE['lg'])
    
    hashtag_font = get_font(TYPE['caption'], False)
    hashtags = "#OpenClaw  #AI 自动化  #token 优化"
    x = center_x(draw, hashtags, hashtag_font)
    draw.text((x, bottom_y), hashtags, fill=COLORS['light'], font=hashtag_font)
    
    img.save('output/00_cover.png', 'PNG')
    print("[OK] 封面")

def generate_page1():
    """第 1 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(TYPE['tiny'], False)
    draw.text((IMG_WIDTH - SPACE['xl'] - 40, SPACE['xl']), "01 / 05", fill=COLORS['light'], font=page_font)
    
    # 章节标题
    title_font = get_font(TYPE['h1'], True)
    title = "策略层优化"
    draw.text((SPACE['xl'], 140), title, fill=COLORS['text'], font=title_font)
    
    # 副标题
    subtitle_font = get_font(TYPE['body'], False)
    draw.text((SPACE['xl'], 220), "节省约 50% token", fill=COLORS['secondary'], font=subtitle_font)
    
    # 分隔线
    draw_line(draw, 270)
    
    # 内容区
    content_y = 330
    
    # 技巧 01
    num_font = get_font(TYPE['caption'], True)
    draw.text((SPACE['xl'], content_y), "01", fill=COLORS['accent'], font=num_font)
    
    title_font = get_font(TYPE['h3'], True)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "脚本优先，AI 后置", fill=COLORS['text'], font=title_font)
    
    # 对比
    content_y += SPACE['lg']
    wrong_font = get_font(TYPE['body'], False)
    draw.text((SPACE['xl'], content_y), "AI 全流程：3000-5000 tokens", fill=COLORS['light'], font=wrong_font)
    
    content_y += SPACE['md']
    right_font = get_font(TYPE['body'], True)
    draw.text((SPACE['xl'], content_y), "脚本计算 + AI 格式化：200-500 tokens", fill=COLORS['text'], font=right_font)
    
    # 效果数据 - 用线分隔
    content_y += SPACE['lg']
    draw_line(draw, content_y, SPACE['xl'], IMG_WIDTH - SPACE['xl'])
    content_y += SPACE['md']
    
    effect_font = get_font(TYPE['caption'], False)
    effects = ["状态刷新 98%", "晚间复盘 96%", "健康检查 98%"]
    eff_x = SPACE['xl']
    for effect in effects:
        draw.text((eff_x, content_y), effect, fill=COLORS['secondary'], font=effect_font)
        bbox = draw.textbbox((0, 0), effect, font=effect_font)
        eff_x += bbox[2] - bbox[0] + SPACE['lg']
    
    # 技巧 02
    content_y += SPACE['xl']
    draw.text((SPACE['xl'], content_y), "02", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "模型分层，按需分配", fill=COLORS['text'], font=title_font)
    
    content_y += SPACE['lg']
    model_font = get_font(TYPE['body'], False)
    draw.text((SPACE['xl'], content_y), "95% 任务 qwen3.5-plus（1 元/10 万）", fill=COLORS['secondary'], font=model_font)
    content_y += SPACE['md']
    draw.text((SPACE['xl'], content_y), "5% 关键任务 gpt-5.4（10 元/10 万）", fill=COLORS['secondary'], font=model_font)
    
    img.save('output/01_strategy.png', 'PNG')
    print("[OK] 01")

def generate_page2():
    """第 2 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    page_font = get_font(TYPE['tiny'], False)
    draw.text((IMG_WIDTH - SPACE['xl'] - 40, SPACE['xl']), "02 / 05", fill=COLORS['light'], font=page_font)
    
    title_font = get_font(TYPE['h1'], True)
    draw.text((SPACE['xl'], 140), "策略层优化（续）", fill=COLORS['text'], font=title_font)
    
    draw_line(draw, 220)
    
    content_y = 280
    
    # 03
    num_font = get_font(TYPE['caption'], True)
    draw.text((SPACE['xl'], content_y), "03", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "会话隔离", fill=COLORS['text'], font=get_font(TYPE['h3'], True))
    
    content_y += SPACE['lg']
    text_font = get_font(TYPE['body'], False)
    draw.text((SPACE['xl'], content_y), "日常任务：main + systemEvent", fill=COLORS['secondary'], font=text_font)
    content_y += SPACE['md']
    draw.text((SPACE['xl'], content_y), "资讯/复盘：isolated + agentTurn", fill=COLORS['text'], font=get_font(TYPE['body'], True))
    content_y += SPACE['md']
    draw.text((SPACE['xl'], content_y), "主会话上下文 < 20%", fill=COLORS['accent'], font=get_font(TYPE['body'], True))
    
    # 04
    content_y += SPACE['xl']
    draw.text((SPACE['xl'], content_y), "04", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "静默成功，失败才报警", fill=COLORS['text'], font=get_font(TYPE['h3'], True))
    
    content_y += SPACE['lg']
    draw.text((SPACE['xl'], content_y), "健康时不推送，失败才告警", fill=COLORS['secondary'], font=text_font)
    content_y += SPACE['md']
    draw.text((SPACE['xl'], content_y), "日均 24 条 → 2-5 条（省 85%）", fill=COLORS['accent'], font=get_font(TYPE['body'], True))
    
    # 05
    content_y += SPACE['xl']
    draw.text((SPACE['xl'], content_y), "05", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "决策短输出", fill=COLORS['text'], font=get_font(TYPE['h3'], True))
    
    # 代码块 - 简约风格
    content_y += SPACE['lg']
    code_bg = '#F5F5F5'
    code_text = "[BUY] 020899 72CNY | gate_consensus | before 15:00"
    code_font = get_font(TYPE['caption'], False)
    bbox = draw.textbbox((0, 0), code_text, font=code_font)
    code_w = bbox[2] - bbox[0] + SPACE['md'] * 2
    code_h = bbox[3] - bbox[1] + SPACE['sm'] * 2
    code_x = SPACE['xl']
    
    draw.rectangle([(code_x, content_y), (code_x + code_w, content_y + code_h)], fill=code_bg)
    draw.text((code_x + SPACE['md'], content_y + SPACE['sm']), code_text, fill=COLORS['text'], font=code_font)
    
    content_y += code_h + SPACE['sm']
    draw.text((SPACE['xl'], content_y), "50 tokens vs 2000 tokens", fill=COLORS['secondary'], font=text_font)
    
    img.save('output/02_strategy2.png', 'PNG')
    print("[OK] 02")

def generate_page3():
    """第 3 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    page_font = get_font(TYPE['tiny'], False)
    draw.text((IMG_WIDTH - SPACE['xl'] - 40, SPACE['xl']), "03 / 05", fill=COLORS['light'], font=page_font)
    
    title_font = get_font(TYPE['h1'], True)
    draw.text((SPACE['xl'], 140), "工具层优化", fill=COLORS['text'], font=title_font)
    
    subtitle_font = get_font(TYPE['body'], False)
    draw.text((SPACE['xl'], 220), "节省约 30% token", fill=COLORS['secondary'], font=subtitle_font)
    
    draw_line(draw, 270)
    
    content_y = 330
    
    # 06
    num_font = get_font(TYPE['caption'], True)
    draw.text((SPACE['xl'], content_y), "06", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "Tavily 搜索", fill=COLORS['text'], font=get_font(TYPE['h3'], True))
    
    content_y += SPACE['lg']
    
    # 对比 - 左右布局
    left_x = SPACE['xl']
    right_x = IMG_WIDTH // 2 + SPACE['md']
    
    # 左
    draw.text((left_x, content_y), "传统搜索", fill=COLORS['light'], font=get_font(TYPE['caption'], False))
    content_y += SPACE['md']
    draw.text((left_x, content_y), "5000+ tokens", fill=COLORS['light'], font=get_font(TYPE['h2'], True))
    
    # 右
    draw.text((right_x, content_y - SPACE['md']), "Tavily", fill=COLORS['accent'], font=get_font(TYPE['caption'], True))
    draw.text((right_x, content_y), "800 tokens", fill=COLORS['accent'], font=get_font(TYPE['h2'], True))
    
    content_y += SPACE['xl']
    draw.text((SPACE['xl'], content_y), "节省 84%", fill=COLORS['accent'], font=get_font(TYPE['h3'], True))
    
    # 07
    content_y += SPACE['xl']
    draw.text((SPACE['xl'], content_y), "07", fill=COLORS['accent'], font=num_font)
    draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), "QMD Memory 检索", fill=COLORS['text'], font=get_font(TYPE['h3'], True))
    
    content_y += SPACE['lg']
    draw.text((SPACE['xl'], content_y), "本地 SQLite + BM25 + 向量检索", fill=COLORS['secondary'], font=get_font(TYPE['body'], False))
    
    content_y += SPACE['md']
    # 对比
    draw.text((SPACE['xl'], content_y), "5000 tokens", fill=COLORS['light'], font=get_font(TYPE['h2'], True))
    draw.text((SPACE['xl'] + 200, content_y), "→", fill=COLORS['light'], font=get_font(TYPE['h2'], False))
    draw.text((SPACE['xl'] + 280, content_y), "300 tokens", fill=COLORS['accent'], font=get_font(TYPE['h2'], True))
    
    content_y += SPACE['md']
    draw.text((SPACE['xl'], content_y), "节省 94%", fill=COLORS['accent'], font=get_font(TYPE['h3'], True))
    
    img.save('output/03_tools.png', 'PNG')
    print("[OK] 03")

def generate_page4():
    """第 4 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    page_font = get_font(TYPE['tiny'], False)
    draw.text((IMG_WIDTH - SPACE['xl'] - 40, SPACE['xl']), "04 / 05", fill=COLORS['light'], font=page_font)
    
    title_font = get_font(TYPE['h1'], True)
    draw.text((SPACE['xl'], 140), "工具层优化（续）", fill=COLORS['text'], font=title_font)
    
    draw_line(draw, 220)
    
    content_y = 280
    
    items = [
        ("08", "文本摘要技能", "长文压缩 90%", None),
        ("09", "本地缓存 + 证据压缩", "JSON 压缩 80%+", "金融 5-15 分钟 · 新闻 1-4 小时 · 规则 24 小时+"),
        ("10", "Memory 分级 + 归档", "检索 token 降 60%", "三层：长期 + 日常 + 归档 · 命中率 80%+"),
    ]
    
    for num, title, highlight, note in items:
        num_font = get_font(TYPE['caption'], True)
        draw.text((SPACE['xl'], content_y), num, fill=COLORS['accent'], font=num_font)
        
        draw.text((SPACE['xl'] + SPACE['lg'], content_y - 4), title, fill=COLORS['text'], font=get_font(TYPE['h3'], True))
        
        content_y += SPACE['md']
        draw.text((SPACE['xl'], content_y), highlight, fill=COLORS['accent'], font=get_font(TYPE['body'], True))
        
        if note:
            content_y += SPACE['sm']
            draw.text((SPACE['xl'], content_y), note, fill=COLORS['secondary'], font=get_font(TYPE['caption'], False))
        
        content_y += SPACE['xl']
    
    img.save('output/04_tools2.png', 'PNG')
    print("[OK] 04")

def generate_page5():
    """第 5 页"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    page_font = get_font(TYPE['tiny'], False)
    draw.text((IMG_WIDTH - SPACE['xl'] - 40, SPACE['xl']), "05 / 05", fill=COLORS['light'], font=page_font)
    
    title_font = get_font(TYPE['h1'], True)
    draw.text((SPACE['xl'], 140), "总体效果", fill=COLORS['text'], font=title_font)
    
    draw_line(draw, 220)
    
    content_y = 280
    
    # 效果对比 - 表格风格
    effects = [
        ("月 token", "100 万", "20 万", "80%"),
        ("主上下文", "80%+", "20%", "75%"),
        ("日均推送", "24 条", "2-5 条", "85%"),
        ("强模型", "50%", "5%", "90%"),
    ]
    
    label_font = get_font(TYPE['body'], False)
    before_font = get_font(TYPE['body'], False)
    after_font = get_font(TYPE['body'], True)
    save_font = get_font(TYPE['caption'], True)
    
    for i, (label, before, after, saving) in enumerate(effects):
        # 标签
        draw.text((SPACE['xl'], content_y), label, fill=COLORS['secondary'], font=label_font)
        
        # 之前
        draw.text((SPACE['xl'] + 150, content_y), before, fill=COLORS['light'], font=before_font)
        
        # 箭头
        draw.text((SPACE['xl'] + 280, content_y), "→", fill=COLORS['light'], font=before_font)
        
        # 之后
        draw.text((SPACE['xl'] + 330, content_y), after, fill=COLORS['accent'], font=after_font)
        
        # 节省
        draw.text((IMG_WIDTH - SPACE['xl'] - 60, content_y), saving, fill=COLORS['accent'], font=save_font)
        
        # 分隔线
        if i < 3:
            draw_line(draw, content_y + SPACE['lg'], SPACE['xl'], IMG_WIDTH - SPACE['xl'])
        
        content_y += SPACE['xl']
    
    # 金句
    content_y += SPACE['md']
    draw_line(draw, content_y, SPACE['xl'], IMG_WIDTH - SPACE['xl'])
    content_y += SPACE['lg']
    
    quote_font = get_font(TYPE['body'], False)
    quote = "省 token 不是为了抠门"
    draw.text((SPACE['xl'], content_y), quote, fill=COLORS['secondary'], font=quote_font)
    
    content_y += SPACE['md']
    quote2_font = get_font(TYPE['h3'], True)
    quote2 = "是为了让系统更可持续"
    draw.text((SPACE['xl'], content_y), quote2, fill=COLORS['text'], font=quote2_font)
    
    # 底部标签
    hashtag_font = get_font(TYPE['tiny'], False)
    hashtags = "#OpenClaw  #AI 自动化  #token 优化  #效率工具"
    draw.text((SPACE['xl'], IMG_HEIGHT - SPACE['xl']), hashtags, fill=COLORS['light'], font=hashtag_font)
    
    img.save('output/05_summary.png', 'PNG')
    print("[OK] 05")

def main():
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("生成高级极简风格...")
    generate_cover()
    generate_page1()
    generate_page2()
    generate_page3()
    generate_page4()
    generate_page5()
    print("完成！")

if __name__ == '__main__':
    main()
