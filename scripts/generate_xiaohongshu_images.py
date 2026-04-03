#!/usr/bin/env python3
"""
小红书图片生成器
生成适合小红书的竖版图片 (1080x1440)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# 配置
IMG_WIDTH = 1080
IMG_HEIGHT = 1440
MARGIN = 80
LINE_HEIGHT = 55

# 颜色配置
COLORS = {
    'bg': '#FFFFFF',
    'primary': '#FF2442',  # 小红书红
    'title': '#1A1A1A',
    'text': '#333333',
    'accent': '#FF6B81',
    'light': '#F5F5F5',
    'code_bg': '#F8F8F8',
}

# 字体路径（需要替换为你系统上的字体）
FONT_PATHS = {
    'title': 'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
    'bold': 'C:\\Windows\\Fonts\\simhei.ttf',
    'normal': 'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
    'mono': 'C:\\Windows\\Fonts\\consola.ttf',
}


def get_font(size, font_type='normal'):
    """获取字体"""
    try:
        return ImageFont.truetype(FONT_PATHS.get(font_type, FONT_PATHS['normal']), size)
    except Exception:
        return ImageFont.load_default()


def create_base_image():
    """创建基础图片"""
    return Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), COLORS['bg'])


def draw_title(draw, text, y_offset):
    """绘制标题"""
    font = get_font(48, 'bold')
    bbox = draw.textbbox((MARGIN, y_offset), text, font=font)
    draw.text((MARGIN, y_offset), text, fill=COLORS['primary'], font=font)
    return bbox[3] + 20


def draw_section_title(draw, text, y_offset):
    """绘制章节标题"""
    font = get_font(36, 'bold')
    bbox = draw.textbbox((MARGIN, y_offset), text, font=font)
    draw.text((MARGIN, y_offset), text, fill=COLORS['title'], font=font)
    return bbox[3] + 15


def draw_text(draw, text, y_offset, font_size=28, color=None, font_type='normal'):
    """绘制普通文本"""
    font = get_font(font_size, font_type)
    color = color or COLORS['text']
    bbox = draw.textbbox((MARGIN, y_offset), text, font=font)
    draw.text((MARGIN, y_offset), text, fill=color, font=font)
    return bbox[3] + 10


def draw_bullet(draw, text, y_offset, bullet='•'):
    """绘制列表项"""
    font = get_font(28, 'normal')
    bullet_text = f"{bullet} {text}"
    bbox = draw.textbbox((MARGIN, y_offset), bullet_text, font=font)
    draw.text((MARGIN, y_offset), bullet_text, fill=COLORS['text'], font=font)
    return bbox[3] + 5


def draw_code_block(draw, code, y_offset):
    """绘制代码块"""
    font = get_font(24, 'mono')
    padding = 20
    lines = code.split('\n')
    
    # 计算代码块尺寸
    max_width = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        max_width = max(max_width, bbox[2] - bbox[0])
    
    code_height = len(lines) * LINE_HEIGHT + padding * 2
    code_width = max_width + padding * 2
    
    # 绘制背景
    x1, y1 = MARGIN, y_offset
    x2, y2 = x1 + code_width, y1 + code_height
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=COLORS['code_bg'])
    
    # 绘制代码
    curr_y = y_offset + padding
    for line in lines:
        draw.text((x1 + padding, curr_y), line, fill=COLORS['text'], font=font)
        curr_y += LINE_HEIGHT
    
    return y2 + 10


def draw_comparison(draw, items, y_offset):
    """绘制对比表格"""
    font = get_font(26, 'normal')
    curr_y = y_offset
    
    for item in items:
        label = item['label']
        before = item['before']
        after = item['after']
        saving = item['saving']
        
        # 绘制标签
        draw.text((MARGIN, curr_y), label, fill=COLORS['text'], font=font)
        
        # 绘制对比
        x_offset = MARGIN + 200
        draw.text((x_offset, curr_y), f"{before} → ", fill='#999999', font=font)
        draw.text((x_offset + 150, curr_y), after, fill=COLORS['primary'], font=get_font(26, 'bold'))
        draw.text((x_offset + 350, curr_y), f"({saving})", fill=COLORS['accent'], font=font)
        
        curr_y += LINE_HEIGHT
    
    return curr_y + 10


def draw_footer(draw, page_num, total_pages, y_offset):
    """绘制页脚"""
    font = get_font(20, 'normal')
    text = f"Page {page_num}/{total_pages} | OpenClaw 省 Token 实战"
    bbox = draw.textbbox((MARGIN, y_offset), text, font=font)
    draw.text((MARGIN, y_offset), text, fill='#999999', font=font)
    return bbox[3]


def generate_cover():
    """生成封面"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    # 主标题
    title_font = get_font(72, 'bold')
    title = "OpenClaw"
    bbox = draw.textbbox((MARGIN, 200), title, font=title_font)
    draw.text((MARGIN, 200), title, fill=COLORS['primary'], font=title_font)
    
    # 副标题
    subtitle_font = get_font(48, 'bold')
    subtitle = "省 Token 实战"
    draw.text((MARGIN, 300), subtitle, fill=COLORS['title'], font=subtitle_font)
    
    # 核心数据
    data_font = get_font(36, 'normal')
    data_points = [
        "月 token：100 万 → 20 万",
        "节省 80%",
        "24 个定时任务",
        "每日自动运行",
    ]
    
    curr_y = 450
    for point in data_points:
        draw.text((MARGIN, curr_y), point, fill=COLORS['text'], font=data_font)
        curr_y += 60
    
    # 底部标签
    tag_font = get_font(28, 'normal')
    tags = "#OpenClaw  #AI 自动化  #token 优化  #效率工具"
    draw.text((MARGIN, IMG_HEIGHT - 150), tags, fill=COLORS['accent'], font=tag_font)
    
    img.save('output/00_cover.png', 'PNG')
    print("✓ 生成封面：00_cover.png")


def generate_page1():
    """生成第 1 页：策略层优化"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    y = draw_title(draw, "💡 策略层优化（省 50%）", 100)
    y += 30
    
    # 技巧 1
    y = draw_section_title(draw, "1️⃣ 脚本优先，AI 后置", y)
    y = draw_text(draw, "❌ 错误：让 AI 读取 JSON → 分析 → 计算 → 输出", y)
    y = draw_text(draw, "   (3000-5000 tokens)", y, font_size=24, color='#999999')
    y = draw_text(draw, "✅ 正确：Python 脚本算好，AI 只格式化", y)
    y = draw_text(draw, "   (200-500 tokens)", y, font_size=24, color='#999999')
    y += 20
    
    y = draw_section_title(draw, "实战效果：", y)
    effects = [
        "• 状态刷新：98% 节省",
        "• 晚间复盘：96% 节省",
        "• 健康检查：98% 节省",
    ]
    for effect in effects:
        y = draw_bullet(draw, effect, y)
    y += 30
    
    # 技巧 2
    y = draw_section_title(draw, "2️⃣ 模型分层，按需分配", y)
    y = draw_text(draw, "95% 任务用 qwen3.5-plus（1 元/10 万 tokens）", y)
    y = draw_text(draw, "5% 关键任务用 gpt-5.4（10 元/10 万 tokens）", y)
    y += 20
    
    y = draw_section_title(draw, "场景分配：", y)
    scenarios = [
        "• 基金交易决策 → gpt-5.4",
        "• 复杂 Debug → gpt-5.4",
        "• 日常 Q&A → qwen3.5-plus",
        "• 状态检查 → qwen3.5-plus",
        "• 资讯整理 → qwen3.5-plus",
    ]
    for scenario in scenarios:
        y = draw_bullet(draw, scenario, y)
    
    draw_footer(draw, 1, 5, IMG_HEIGHT - 80)
    img.save('output/01_strategy.png', 'PNG')
    print("✓ 生成第 1 页：01_strategy.png")


def generate_page2():
    """生成第 2 页：策略层优化续"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    y = draw_title(draw, "💡 策略层优化（续）", 100)
    y += 30
    
    # 技巧 3
    y = draw_section_title(draw, "3️⃣ 会话隔离，不污染主上下文", y)
    y = draw_text(draw, "日常任务：main + systemEvent（轻量）", y)
    y = draw_text(draw, "资讯/复盘：isolated + agentTurn（独立）", y)
    y = draw_text(draw, "效果：主会话上下文长期保持<20%", y, font_size=24, color=COLORS['primary'])
    y += 30
    
    # 技巧 4
    y = draw_section_title(draw, "4️⃣ 静默成功，失败才报警", y)
    y = draw_text(draw, "健康时不推送，失败才告警", y)
    y = draw_text(draw, "推送频率：日均 24 条 → 2-5 条（省 85%）", y, font_size=24, color=COLORS['primary'])
    y += 30
    
    # 技巧 5
    y = draw_section_title(draw, "5️⃣ 决策短输出，拒绝废话", y)
    y = draw_text(draw, "❌ 冗长版（2000 tokens）：", y)
    y = draw_code_block(draw, "根据当前市场分析，考虑到...\n综合各方面因素，我们建议...", y)
    y = draw_text(draw, "✅ 精简版（50 tokens）：", y)
    y = draw_code_block(draw, "[BUY] 020899 72CNY | gate_consensus | before 15:00", y)
    
    draw_footer(draw, 2, 5, IMG_HEIGHT - 80)
    img.save('output/02_strategy2.png', 'PNG')
    print("✓ 生成第 2 页：02_strategy2.png")


def generate_page3():
    """生成第 3 页：工具层优化"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    y = draw_title(draw, "🔧 工具层优化（省 30%）", 100)
    y += 30
    
    # 技巧 6
    y = draw_section_title(draw, "6️⃣ Tavily 搜索（AI 优化）", y)
    y = draw_text(draw, "传统搜索：返回 10 条链接 → AI 逐个读取", y)
    y = draw_text(draw, "→ 5000+ tokens", y, font_size=24, color='#999999')
    y = draw_text(draw, "Tavily：直接返回精炼摘要", y)
    y = draw_text(draw, "→ 800 tokens（省 84%）", y, font_size=24, color=COLORS['primary'])
    y += 30
    
    # 技巧 7
    y = draw_section_title(draw, "7️⃣ QMD Memory 检索（本地 MCP）", y)
    y = draw_text(draw, "原理：本地 SQLite + BM25 + 向量检索", y)
    y = draw_text(draw, "传统检索：加载全部 memory → 5000 tokens", y)
    y = draw_text(draw, "QMD：只加载相关片段 → 300 tokens", y)
    y = draw_text(draw, "节省：94%", y, font_size=24, color=COLORS['primary'])
    y += 20
    
    y = draw_section_title(draw, "配置示例：", y)
    config = '''{
  "compaction": { "mode": "aggressive" },
  "mcpServers": {
    "qmd": {
      "command": "wsl",
      "args": ["node", "/path/to/qmd.js", "mcp"]
    }
  }
}'''
    y = draw_code_block(draw, config, y)
    
    draw_footer(draw, 3, 5, IMG_HEIGHT - 80)
    img.save('output/03_tools.png', 'PNG')
    print("✓ 生成第 3 页：03_tools.png")


def generate_page4():
    """生成第 4 页：工具层优化续"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    y = draw_title(draw, "🔧 工具层优化（续）", 100)
    y += 30
    
    # 技巧 8
    y = draw_section_title(draw, "8️⃣ 文本摘要技能", y)
    y = draw_text(draw, "长文压缩 90%", y)
    y = draw_text(draw, "适合：研报、新闻、长对话总结", y)
    y += 30
    
    # 技巧 9
    y = draw_section_title(draw, "9️⃣ 本地缓存 + 证据压缩", y)
    y = draw_text(draw, "• 运行时缓存避免重复抓取", y)
    y = draw_text(draw, "• JSON 压缩 80%+", y)
    y = draw_text(draw, "• 决策输出压缩 90%", y)
    y += 20
    
    y = draw_section_title(draw, "缓存 TTL 建议：", y)
    ttl_items = [
        "• 金融数据：5-15 分钟",
        "• 新闻资讯：1-4 小时",
        "• 规则配置：24 小时+",
    ]
    for item in ttl_items:
        y = draw_bullet(draw, item, y)
    y += 30
    
    # 技巧 10
    y = draw_section_title(draw, "🔟 Memory 分级 + 自动归档", y)
    y = draw_text(draw, "三层结构：", y)
    y = draw_text(draw, "• MEMORY.md - 长期记忆（<2KB）", y)
    y = draw_text(draw, "• memory/YYYY-MM-DD.md - 日常记忆（7 天）", y)
    y = draw_text(draw, "• archive/ - 自动归档", y)
    y = draw_text(draw, "效果：检索命中率 80%+，检索 token 降 60%", y, font_size=24, color=COLORS['primary'])
    
    draw_footer(draw, 4, 5, IMG_HEIGHT - 80)
    img.save('output/04_tools2.png', 'PNG')
    print("✓ 生成第 4 页：04_tools2.png")


def generate_page5():
    """生成第 5 页：效果对比和避坑"""
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    y = draw_title(draw, "📊 总体效果对比", 100)
    y += 30
    
    # 效果对比
    effects = [
        {'label': '月 token', 'before': '100 万', 'after': '20 万', 'saving': '省 80%'},
        {'label': '主上下文', 'before': '80%+', 'after': '20%', 'saving': '省 75%'},
        {'label': '日均推送', 'before': '24 条', 'after': '2-5 条', 'saving': '省 85%'},
        {'label': '强模型使用', 'before': '50%', 'after': '5%', 'saving': '省 90%'},
    ]
    y = draw_comparison(draw, effects, y)
    y += 40
    
    # 避坑指南
    y = draw_section_title(draw, "⚠️ 避坑指南", y)
    pitfalls = [
        "1. 不要过度配置 MCP（每个都占内存）",
        "2. Skills 不是越多越好（定期审查）",
        "3. 缓存要设置 TTL（按数据类型）",
        "4. Compaction 不要过度（关键对话前临时关闭）",
        "5. 不要为了省 token 牺牲用户体验",
    ]
    for pitfall in pitfalls:
        y = draw_bullet(draw, pitfall, y)
    y += 40
    
    # 核心心法
    y = draw_section_title(draw, "🎯 核心心法", y)
    principles = [
        "脚本优先 | 模型分层 | 上下文隔离",
        "静默成功 | 输出精简 | Tavily 搜索",
        "QMD 检索 | 本地缓存 | Memory 分级",
        "自动切换 | 压缩证据 | 定期审查",
    ]
    for principle in principles:
        y = draw_text(draw, principle, y, font_size=24, color=COLORS['accent'])
    
    # 底部金句
    quote = "省 token 不是为了抠门，是为了让系统更可持续。"
    y = draw_text(draw, quote, IMG_HEIGHT - 150, font_size=28, color=COLORS['primary'], font_type='bold')
    
    draw_footer(draw, 5, 5, IMG_HEIGHT - 80)
    img.save('output/05_summary.png', 'PNG')
    print("✓ 生成第 5 页：05_summary.png")


def main():
    """主函数"""
    # 创建输出目录
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    print("开始生成小红书图片...")
    print("=" * 50)
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    generate_cover()
    generate_page1()
    generate_page2()
    generate_page3()
    generate_page4()
    generate_page5()
    
    print("=" * 50)
    print("✅ 完成！共生成 6 张图片")
    print("输出目录：output/")


if __name__ == '__main__':
    main()
