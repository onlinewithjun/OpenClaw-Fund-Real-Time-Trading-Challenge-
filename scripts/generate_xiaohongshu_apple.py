#!/usr/bin/env python3
"""
小红书图片生成器 - 苹果极简风格
1080x1440 竖版，大量留白，简洁排版
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# 配置
IMG_WIDTH = 1080
IMG_HEIGHT = 1440

# 苹果风配色
COLORS = {
    'bg': '#FFFFFF',
    'text': '#1D1D1F',      # 苹果深灰
    'secondary': '#86868B',  # 浅灰
    'accent': '#0071E3',     # 苹果蓝
    'line': '#D2D2D7',       # 分隔线
}

# 字体
FONT_PATHS = {
    'light': 'C:\\Windows\\Fonts\\msyh.ttc',     # 微软雅黑 Light
    'regular': 'C:\\Windows\\Fonts\\msyh.ttc',   # 微软雅黑
    'bold': 'C:\\Windows\\Fonts\\msyhbd.ttc',    # 微软雅黑 Bold
}


def get_font(size, weight='regular'):
    """获取字体"""
    try:
        return ImageFont.truetype(FONT_PATHS.get(weight, FONT_PATHS['regular']), size)
    except Exception:
        return ImageFont.load_default()


def center_text(draw, text, y, font, color=None):
    """居中绘制文本"""
    color = color or COLORS['text']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (IMG_WIDTH - text_width) // 2
    draw.text((x, y), text, fill=color, font=font)
    return bbox[3] - bbox[1] + y


def create_base():
    """创建白色背景"""
    return Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), COLORS['bg'])


def draw_line(draw, y, width=None):
    """绘制分隔线"""
    width = width or IMG_WIDTH - 160
    x1 = (IMG_WIDTH - width) // 2
    draw.line([(x1, y), (x1 + width, y)], fill=COLORS['line'], width=1)


def generate_cover():
    """封面 - 极简风格"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 顶部小标签
    tag_font = get_font(20, 'light')
    tag_text = "OpenClaw 实战分享"
    center_text(draw, tag_text, 120, tag_font, COLORS['secondary'])
    
    # 主标题 - 超大字号
    title_font = get_font(88, 'bold')
    title = "OpenClaw"
    center_text(draw, title, 280, title_font, COLORS['text'])
    
    # 副标题
    subtitle_font = get_font(42, 'regular')
    subtitle = "省 Token 实战"
    center_text(draw, subtitle, 400, subtitle_font, COLORS['secondary'])
    
    # 分隔线
    draw_line(draw, 480, 400)
    
    # 核心数据 - 放大显示
    data_font = get_font(56, 'bold')
    data_color = COLORS['accent']
    
    data_items = [
        ("100 万", "→", "20 万"),
        ("月 token 消耗", "", ""),
    ]
    
    curr_y = 560
    # 第一行数据
    bbox = draw.textbbox((0, 0), "100 万", font=data_font)
    data_h = bbox[3] - bbox[1]
    
    # 100 万
    text1 = "100 万"
    bbox1 = draw.textbbox((0, 0), text1, font=data_font)
    w1 = bbox1[2] - bbox1[0]
    draw.text(((IMG_WIDTH//2 - 100 - w1), curr_y), text1, fill=COLORS['secondary'], font=data_font)
    
    # 箭头
    arrow_font = get_font(42, 'light')
    draw.text(((IMG_WIDTH//2 - 30), curr_y + 8), "→", fill=COLORS['secondary'], font=arrow_font)
    
    # 20 万
    text2 = "20 万"
    bbox2 = draw.textbbox((0, 0), text2, font=data_font)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((IMG_WIDTH//2 + 100), curr_y), text2, fill=data_color, font=data_font)
    
    # 说明文字
    curr_y += 80
    desc_font = get_font(28, 'regular')
    center_text(draw, "月 token 消耗", curr_y, desc_font, COLORS['secondary'])
    
    # 其他数据
    curr_y += 100
    small_font = get_font(24, 'light')
    stats = [
        "节省 80%  •  24 个定时任务  •  每日自动运行",
    ]
    for stat in stats:
        center_text(draw, stat, curr_y, small_font, COLORS['secondary'])
        curr_y += 40
    
    # 底部标签
    tag_font = get_font(18, 'light')
    center_text(draw, "#OpenClaw  #AI 自动化  #token 优化", IMG_HEIGHT - 100, tag_font, COLORS['secondary'])
    
    img.save('output/00_cover.png', 'PNG')
    print("[OK] 封面")


def generate_page1():
    """第 1 页 - 策略层"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(16, 'light')
    center_text(draw, "1 / 5", 80, page_font, COLORS['secondary'])
    
    # 章节标题
    title_font = get_font(48, 'bold')
    center_text(draw, "策略层优化", 160, title_font, COLORS['text'])
    
    # 副标题
    subtitle_font = get_font(24, 'light')
    center_text(draw, "节省约 50% token", 240, subtitle_font, COLORS['secondary'])
    
    # 分隔线
    draw_line(draw, 290, 300)
    
    # 内容 - 对比式
    curr_y = 360
    
    # 技巧 1
    num_font = get_font(32, 'bold')
    draw.text((80, curr_y), "01", fill=COLORS['accent'], font=num_font)
    
    text_font = get_font(28, 'regular')
    center_text(draw, "脚本优先，AI 后置", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    wrong_font = get_font(22, 'light')
    center_text(draw, "❌ AI 全流程：3000-5000 tokens", curr_y, wrong_font, COLORS['secondary'])
    
    curr_y += 40
    right_font = get_font(22, 'regular')
    center_text(draw, "✅ 脚本计算 + AI 格式化：200-500 tokens", curr_y, right_font, COLORS['text'])
    
    # 效果数据
    curr_y += 80
    draw_line(draw, curr_y, 400)
    curr_y += 40
    
    effect_font = get_font(20, 'regular')
    effects = [
        "状态刷新  98% 节省",
        "晚间复盘  96% 节省",
        "健康检查  98% 节省",
    ]
    for effect in effects:
        center_text(draw, effect, curr_y, effect_font, COLORS['text'])
        curr_y += 36
    
    # 技巧 2
    curr_y += 40
    draw.text((80, curr_y), "02", fill=COLORS['accent'], font=num_font)
    center_text(draw, "模型分层，按需分配", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    model_font = get_font(22, 'light')
    center_text(draw, "95% 任务 qwen3.5-plus  •  5% 关键任务 gpt-5.4", curr_y, model_font, COLORS['secondary'])
    
    # 底部分隔
    draw_line(draw, IMG_HEIGHT - 120, 200)
    
    img.save('output/01_strategy.png', 'PNG')
    print("[OK] 第 1 页 - 策略层")


def generate_page2():
    """第 2 页 - 策略层续"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(16, 'light')
    center_text(draw, "2 / 5", 80, page_font, COLORS['secondary'])
    
    # 章节标题
    title_font = get_font(48, 'bold')
    center_text(draw, "策略层优化（续）", 160, title_font, COLORS['text'])
    
    # 分隔线
    draw_line(draw, 240, 300)
    
    curr_y = 300
    
    # 技巧 3
    num_font = get_font(32, 'bold')
    draw.text((80, curr_y), "03", fill=COLORS['accent'], font=num_font)
    
    text_font = get_font(28, 'regular')
    center_text(draw, "会话隔离", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    desc_font = get_font(22, 'light')
    center_text(draw, "日常任务 main + systemEvent（轻量）", curr_y, desc_font, COLORS['secondary'])
    curr_y += 36
    center_text(draw, "资讯/复盘 isolated + agentTurn（独立）", curr_y, desc_font, COLORS['secondary'])
    curr_y += 40
    result_font = get_font(22, 'regular')
    center_text(draw, "主会话上下文 < 20%", curr_y, result_font, COLORS['accent'])
    
    # 技巧 4
    curr_y += 80
    draw.text((80, curr_y), "04", fill=COLORS['accent'], font=num_font)
    center_text(draw, "静默成功，失败才报警", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    center_text(draw, "健康时不推送  •  失败才告警", curr_y, desc_font, COLORS['secondary'])
    curr_y += 40
    center_text(draw, "日均推送 24 条 → 2-5 条（省 85%）", curr_y, result_font, COLORS['accent'])
    
    # 技巧 5
    curr_y += 80
    draw.text((80, curr_y), "05", fill=COLORS['accent'], font=num_font)
    center_text(draw, "决策短输出", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    # 代码块风格
    code_bg = '#F5F5F7'
    code_padding = 30
    code_text = "[BUY] 020899 72CNY | gate_consensus | before 15:00"
    code_font = get_font(20, 'regular')
    bbox = draw.textbbox((0, 0), code_text, font=code_font)
    code_w = bbox[2] - bbox[0] + code_padding * 2
    code_h = bbox[3] - bbox[1] + code_padding
    code_x = (IMG_WIDTH - code_w) // 2
    
    # 绘制代码背景
    draw.rounded_rectangle(
        [(code_x, curr_y), (code_x + code_w, curr_y + code_h)],
        radius=8,
        fill=code_bg
    )
    center_text(draw, code_text, curr_y + code_padding//2, code_font, COLORS['text'])
    
    curr_y += code_h + 20
    center_text(draw, "50 tokens（vs 2000 tokens）", curr_y, desc_font, COLORS['secondary'])
    
    # 底部分隔
    draw_line(draw, IMG_HEIGHT - 120, 200)
    
    img.save('output/02_strategy2.png', 'PNG')
    print("[OK] 第 2 页 - 策略层续")


def generate_page3():
    """第 3 页 - 工具层"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(16, 'light')
    center_text(draw, "3 / 5", 80, page_font, COLORS['secondary'])
    
    # 章节标题
    title_font = get_font(48, 'bold')
    center_text(draw, "工具层优化", 160, title_font, COLORS['text'])
    
    # 副标题
    subtitle_font = get_font(24, 'light')
    center_text(draw, "节省约 30% token", 240, subtitle_font, COLORS['secondary'])
    
    # 分隔线
    draw_line(draw, 290, 300)
    
    curr_y = 360
    
    # 技巧 6
    num_font = get_font(32, 'bold')
    draw.text((80, curr_y), "06", fill=COLORS['accent'], font=num_font)
    
    text_font = get_font(28, 'regular')
    center_text(draw, "Tavily 搜索", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    desc_font = get_font(22, 'light')
    center_text(draw, "AI 优化的搜索引擎", curr_y, desc_font, COLORS['secondary'])
    
    curr_y += 50
    # 对比数据
    data_font = get_font(32, 'bold')
    small_font = get_font(18, 'light')
    
    # 传统搜索
    draw.text((IMG_WIDTH//2 - 180, curr_y), "传统搜索", fill=COLORS['secondary'], font=small_font)
    center_text(draw, "5000+ tokens", curr_y + 30, data_font, COLORS['secondary'])
    
    # 箭头
    arrow_font = get_font(28, 'light')
    draw.text((IMG_WIDTH//2 - 20, curr_y + 32), "→", fill=COLORS['secondary'], font=arrow_font)
    
    # Tavily
    draw.text((IMG_WIDTH//2 + 140, curr_y), "Tavily", fill=COLORS['accent'], font=small_font)
    center_text(draw, "800 tokens", curr_y + 30, data_font, COLORS['accent'])
    
    curr_y += 90
    center_text(draw, "节省 84%", curr_y, text_font, COLORS['accent'])
    
    # 技巧 7
    curr_y += 80
    draw.text((80, curr_y), "07", fill=COLORS['accent'], font=num_font)
    center_text(draw, "QMD Memory 检索", curr_y, text_font, COLORS['text'])
    
    curr_y += 60
    center_text(draw, "本地 SQLite + BM25 + 向量检索", curr_y, desc_font, COLORS['secondary'])
    
    curr_y += 50
    # 对比
    center_text(draw, "5000 tokens  →  300 tokens", curr_y, data_font, COLORS['text'])
    curr_y += 40
    center_text(draw, "节省 94%", curr_y, text_font, COLORS['accent'])
    
    # 底部分隔
    draw_line(draw, IMG_HEIGHT - 120, 200)
    
    img.save('output/03_tools.png', 'PNG')
    print("[OK] 第 3 页 - 工具层")


def generate_page4():
    """第 4 页 - 工具层续"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(16, 'light')
    center_text(draw, "4 / 5", 80, page_font, COLORS['secondary'])
    
    # 章节标题
    title_font = get_font(48, 'bold')
    center_text(draw, "工具层优化（续）", 160, title_font, COLORS['text'])
    
    # 分隔线
    draw_line(draw, 240, 300)
    
    curr_y = 300
    
    # 技巧 8
    num_font = get_font(32, 'bold')
    draw.text((80, curr_y), "08", fill=COLORS['accent'], font=num_font)
    text_font = get_font(28, 'regular')
    center_text(draw, "文本摘要技能", curr_y, text_font, COLORS['text'])
    curr_y += 60
    desc_font = get_font(22, 'light')
    center_text(draw, "长文压缩 90%", curr_y, desc_font, COLORS['accent'])
    
    # 技巧 9
    curr_y += 80
    draw.text((80, curr_y), "09", fill=COLORS['accent'], font=num_font)
    center_text(draw, "本地缓存 + 证据压缩", curr_y, text_font, COLORS['text'])
    curr_y += 60
    center_text(draw, "JSON 压缩 80%+  •  决策输出压缩 90%", curr_y, desc_font, COLORS['secondary'])
    
    # 缓存 TTL
    curr_y += 50
    ttl_font = get_font(18, 'light')
    ttl_items = [
        "金融数据 5-15 分钟  •  新闻资讯 1-4 小时  •  规则配置 24 小时+",
    ]
    for item in ttl_items:
        center_text(draw, item, curr_y, ttl_font, COLORS['secondary'])
        curr_y += 32
    
    # 技巧 10
    curr_y += 60
    draw.text((80, curr_y), "10", fill=COLORS['accent'], font=num_font)
    center_text(draw, "Memory 分级 + 自动归档", curr_y, text_font, COLORS['text'])
    curr_y += 60
    center_text(draw, "三层结构：长期记忆 + 日常记忆 + 归档", curr_y, desc_font, COLORS['secondary'])
    curr_y += 40
    center_text(draw, "检索命中率 80%+  •  检索 token 降 60%", curr_y, desc_font, COLORS['accent'])
    
    # 底部分隔
    draw_line(draw, IMG_HEIGHT - 120, 200)
    
    img.save('output/04_tools2.png', 'PNG')
    print("[OK] 第 4 页 - 工具层续")


def generate_page5():
    """第 5 页 - 总结"""
    img = create_base()
    draw = ImageDraw.Draw(img)
    
    # 页码
    page_font = get_font(16, 'light')
    center_text(draw, "5 / 5", 80, page_font, COLORS['secondary'])
    
    # 章节标题
    title_font = get_font(48, 'bold')
    center_text(draw, "总体效果", 160, title_font, COLORS['text'])
    
    # 分隔线
    draw_line(draw, 240, 300)
    
    curr_y = 300
    
    # 效果对比 - 大数字
    data_font = get_font(56, 'bold')
    label_font = get_font(22, 'light')
    
    effects = [
        ("月 token", "100 万", "20 万", "80%"),
        ("主上下文", "80%+", "20%", "75%"),
        ("日均推送", "24 条", "2-5 条", "85%"),
        ("强模型", "50%", "5%", "90%"),
    ]
    
    for label, before, after, saving in effects:
        # 标签
        draw.text((80, curr_y + 10), label, fill=COLORS['secondary'], font=label_font)
        
        # 之前
        before_font = get_font(32, 'light')
        bbox = draw.textbbox((0, 0), before, font=before_font)
        before_w = bbox[2] - bbox[0]
        draw.text((IMG_WIDTH//2 - 150 - before_w, curr_y), before, fill=COLORS['secondary'], font=before_font)
        
        # 箭头
        draw.text((IMG_WIDTH//2 - 50, curr_y + 5), "→", fill=COLORS['line'], font=before_font)
        
        # 之后
        after_font = get_font(32, 'bold')
        draw.text((IMG_WIDTH//2 + 100, curr_y), after, fill=COLORS['accent'], font=after_font)
        
        # 节省
        save_font = get_font(28, 'bold')
        save_w = draw.textbbox((0, 0), saving, font=save_font)[2]
        draw.text((IMG_WIDTH - 120 - save_w, curr_y), saving, fill=COLORS['accent'], font=save_font)
        
        curr_y += 70
    
    # 底部分隔
    curr_y += 40
    draw_line(draw, curr_y, 400)
    
    # 金句
    curr_y += 60
    quote_font = get_font(28, 'light')
    quote = "省 token 不是为了抠门"
    center_text(draw, quote, curr_y, quote_font, COLORS['secondary'])
    curr_y += 45
    quote_font2 = get_font(28, 'regular')
    quote2 = "是为了让系统更可持续"
    center_text(draw, quote2, curr_y, quote_font2, COLORS['text'])
    
    # 标签
    tag_font = get_font(16, 'light')
    center_text(draw, "#OpenClaw  #AI 自动化  #token 优化  #效率工具", IMG_HEIGHT - 80, tag_font, COLORS['secondary'])
    
    img.save('output/05_summary.png', 'PNG')
    print("[OK] 第 5 页 - 总结")


def main():
    """主函数"""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("生成苹果风小红书图片...")
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
