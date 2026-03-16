# -*- coding: utf-8 -*-
"""
基金实盘收益更新脚本 - 1000 元挑战
查询持仓基金今日净值，计算当日盈亏和累计盈亏
输出格式化报告
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import sys

# 设置标准输出为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 持仓信息 (基于 fund-holdings.md)
# 建仓日期：2026-03-04
holdings = {
    '020899': {
        'name': '天弘中证通信设备',
        'amount': 350,  # 初始投资金额
        'purchase_nav': 2.83,  # 建仓估算净值
        'type': '科技/通信'
    },
    '017192': {
        'name': '天弘中证工业有色金属',
        'amount': 350,
        'purchase_nav': 2.20,  # 修正后的建仓估算净值
        'type': '周期/资源'
    },
    '002611': {
        'name': '博时黄金 ETF 联接',
        'amount': 200,  # 减仓后剩余 (原 300 元，卖出 100 元)
        'purchase_nav': 3.60,  # 建仓估算净值
        'type': '避险/商品'
    }
}

# 现金仓位
cash = 100  # 减仓黄金 ETF 后保留的现金

def get_fund_nav(fund_code):
    """获取基金最新净值数据"""
    try:
        df = ak.fund_open_fund_info_em(symbol=fund_code, indicator='单位净值走势', period='近 1 月')
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else None
        return {
            'date': latest['净值日期'],
            'nav': float(latest['单位净值']),
            'change': float(latest['日增长率']),
            'prev_nav': float(prev['单位净值']) if prev is not None else None
        }
    except Exception as e:
        print(f"获取基金 {fund_code} 数据失败：{e}")
        return None

def calculate_pnl(fund_code, holding_info, nav_data):
    """计算单只基金盈亏"""
    if nav_data is None:
        return None
    
    # 计算份额 (基于建仓净值)
    shares = holding_info['amount'] / holding_info['purchase_nav']
    
    # 当前市值
    current_value = shares * nav_data['nav']
    
    # 累计盈亏
    cumulative_pnl = current_value - holding_info['amount']
    
    # 当日盈亏 (基于昨日市值)
    if nav_data['prev_nav']:
        prev_value = shares * nav_data['prev_nav']
        daily_pnl = current_value - prev_value
    else:
        daily_pnl = 0
    
    return {
        'code': fund_code,
        'name': holding_info['name'],
        'type': holding_info['type'],
        'amount': holding_info['amount'],
        'shares': shares,
        'purchase_nav': holding_info['purchase_nav'],
        'current_nav': nav_data['nav'],
        'nav_date': str(nav_data['date']),
        'nav_change': nav_data['change'],
        'current_value': current_value,
        'daily_pnl': daily_pnl,
        'cumulative_pnl': cumulative_pnl,
        'daily_pnl_pct': (daily_pnl / (shares * nav_data['prev_nav']) * 100) if nav_data['prev_nav'] else 0,
        'cumulative_pnl_pct': (cumulative_pnl / holding_info['amount']) * 100
    }

def generate_telegram_report(results, summary):
    """生成 Telegram 格式报告"""
    report = []
    report.append("【💰 1000 元挑战 - 收益更新】")
    report.append(f"📅 更新时点：2026-03-05 20:00 (净值披露后)")
    report.append(f"📊 交易日：Day 2 (建仓后第 1 个交易日)")
    report.append("")
    report.append("【持仓详情】")
    report.append("")
    
    for r in results:
        report.append(f"▫️ {r['name']} ({r['code']})")
        report.append(f"   类型：{r['type']}")
        report.append(f"   净值日期：{r['nav_date']}")
        report.append(f"   当前净值：{r['current_nav']:.4f} ({r['nav_change']:+.2f}%)")
        report.append(f"   持仓市值：{r['current_value']:.2f} 元")
        report.append(f"   当日盈亏：{r['daily_pnl']:+.2f} 元 ({r['daily_pnl_pct']:+.2f}%)")
        report.append(f"   累计盈亏：{r['cumulative_pnl']:+.2f} 元 ({r['cumulative_pnl_pct']:+.2f}%)")
        report.append("")
    
    report.append("【汇总】")
    report.append(f"▫️ 基金市值：{summary['fund_value']:.2f} 元")
    report.append(f"▫️ 现金仓位：{cash:.2f} 元")
    report.append(f"▫️ 总资产：{summary['total_value']:.2f} 元")
    report.append(f"▫️ 当日盈亏：{summary['daily_pnl']:+.2f} 元 ({summary['daily_pnl_pct']:+.2f}%)")
    report.append(f"▫️ 累计盈亏：{summary['cumulative_pnl']:+.2f} 元 ({summary['cumulative_pnl_pct']:+.2f}%)")
    report.append("")
    report.append("【仓位占比】")
    for r in results:
        ratio = r['current_value'] / summary['total_value'] * 100
        report.append(f"▫️ {r['name']}: {ratio:.1f}%")
    cash_ratio = cash / summary['total_value'] * 100
    report.append(f"▫️ 现金：{cash_ratio:.1f}%")
    report.append("")
    report.append("⚠️ 场外基金 T+1 确认，3 月 5 日净值将于今晚公布，明日可见")
    
    return "\n".join(report)

def main():
    results = []
    total_value = 0
    total_daily_pnl = 0
    total_cumulative_pnl = 0
    total_invested = 0
    
    for fund_code, holding_info in holdings.items():
        nav_data = get_fund_nav(fund_code)
        
        if nav_data:
            result = calculate_pnl(fund_code, holding_info, nav_data)
            results.append(result)
            
            total_value += result['current_value']
            total_daily_pnl += result['daily_pnl']
            total_cumulative_pnl += result['cumulative_pnl']
            total_invested += holding_info['amount']
    
    # 加上现金仓位
    total_value += cash
    total_invested += cash
    
    summary = {
        'total_value': total_value,
        'fund_value': total_value - cash,
        'daily_pnl': total_daily_pnl,
        'daily_pnl_pct': total_daily_pnl / (total_invested - cash) * 100,
        'cumulative_pnl': total_cumulative_pnl,
        'cumulative_pnl_pct': total_cumulative_pnl / total_invested * 100
    }
    
    # 生成 Telegram 报告
    report = generate_telegram_report(results, summary)
    
    # 输出到文件
    with open('fund_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 输出 JSON 数据用于后续处理
    data = {
        'date': '2026-03-05',
        'results': results,
        'summary': summary,
        'cash': cash
    }
    with open('fund_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(report)
    print("\n[报告已保存至 fund_report.txt 和 fund_data.json]")
    
    return report, data

if __name__ == '__main__':
    report, data = main()
