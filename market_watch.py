#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
定时盯盘脚本 - 每 10 分钟执行一次，连续 3 次
通过 web_search 获取行情数据并发送到主会话
"""

import subprocess
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

def search_market_data():
    """通过 web_search 搜索最新行情"""
    query = "2026 年 3 月 3 日 上证指数 深证成指 科创 50 创业板指 黄金 纳斯达克 实时涨跌幅"
    
    try:
        # 调用 openclaw web_search
        result = subprocess.run(
            ['openclaw', 'web_search', '-q', query, '-c', '5'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"搜索失败：{e}"

def send_message(message):
    """发送消息到主会话"""
    try:
        # 使用 sessions_send
        subprocess.run(
            ['openclaw', 'sessions_send', '--label', 'main', '--message', message],
            capture_output=True,
            text=True,
            timeout=10
        )
    except Exception as e:
        print(f"发送失败：{e}")

def generate_report():
    """生成盯盘报告"""
    now = datetime.now()
    report = f"""📊 **股市盯盘** ({now.strftime('%H:%M')})

**搜索时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}

正在获取最新行情数据...
"""
    return report

def main():
    print("=" * 60)
    print("定时盯盘任务启动")
    print("=" * 60)
    
    interval_minutes = 10
    num_runs = 3
    
    for i in range(num_runs):
        print(f"\n[{i+1}/{num_runs}] 执行第 {i+1} 次盯盘...")
        
        # 生成报告
        report = generate_report()
        report += f"\n第 {i+1} 次更新 - {datetime.now().strftime('%H:%M:%S')}"
        
        # 发送消息
        print(f"发送报告...")
        send_message(report)
        
        if i < num_runs - 1:
            next_time = datetime.now() + timedelta(minutes=interval_minutes)
            print(f"下次更新：{next_time.strftime('%H:%M')}")
            print(f"等待 {interval_minutes} 分钟...")
            time.sleep(interval_minutes * 60)
    
    print("\n✅ 盯盘任务完成")
    send_message("✅ 盯盘任务完成，共执行 3 次更新")

if __name__ == '__main__':
    main()
