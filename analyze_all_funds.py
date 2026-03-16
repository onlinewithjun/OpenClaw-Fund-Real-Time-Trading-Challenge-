#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析所有持仓基金的实时涨跌预估
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import re
import csv
from datetime import datetime

session = requests.Session()
session.trust_env = False

# 基金重仓股配置（根据最新季报）
FUND_HOLDINGS = {
    '002963': {  # 易方达黄金 ETF 联接 C
        'name': '易方达黄金 ETF 联接 C',
        'type': '黄金',
        'holdings': [('黄金', 'GC=F', 95.0)]
    },
    '021485': {  # 景顺长城科创 50 联接 C
        'name': '景顺长城科创 50 联接 C',
        'type': '科创 50',
        'holdings': [('科创 50ETF', '588000', 95.0)]
    },
    '019449': {  # 摩根日本精选股票 (QDII)C
        'name': '摩根日本精选股票 (QDII)C',
        'type': '日本股票',
        'holdings': [('日经 225', 'gb_N225', 90.0)]
    },
    '012733': {  # 易方达人工智能 ETF 联接 A
        'name': '易方达人工智能 ETF 联接 A',
        'type': '人工智能',
        'holdings': [
            ('科大讯飞', '002230', 8.5), ('海康威视', '002415', 7.2),
            ('大华股份', '002236', 6.8), ('韦尔股份', '603501', 5.9),
            ('金山办公', '688111', 5.5), ('中科曙光', '603019', 5.2),
            ('浪潮信息', '000977', 4.8), ('虹软科技', '688088', 4.5),
            ('当虹科技', '688039', 3.8), ('云从科技', '688327', 3.5)
        ]
    },
    '011612': {  # 华夏科创 50ETF 联接 A
        'name': '华夏科创 50ETF 联接 A',
        'type': '科创 50',
        'holdings': [('科创 50ETF', '588000', 95.0)]
    },
    '000217': {  # 华安黄金 ETF 联接 C
        'name': '华安黄金 ETF 联接 C',
        'type': '黄金',
        'holdings': [('黄金', 'GC=F', 95.0)]
    },
    '006479': {  # 广发纳斯达克 100ETF 联接 (QDII)C
        'name': '广发纳斯达克 100ETF 联接 (QDII)C',
        'type': '纳斯达克',
        'holdings': [('纳斯达克 100', 'gb_NDX', 95.0)]
    },
    '003376': {  # 广发中债 7-10 年期国开行债券指数 A
        'name': '广发中债 7-10 年期国开行债券指数 A',
        'type': '债券',
        'holdings': [('中债 7-10 年', 'CBA02701', 0.05)]  # 债券波动小
    },
    '008887': {  # 华夏国证半导体芯片 ETF 联接 A
        'name': '华夏国证半导体芯片 ETF 联接 A',
        'type': '半导体',
        'holdings': [
            ('中芯国际', '688981', 9.2), ('韦尔股份', '603501', 7.8),
            ('卓胜微', '300782', 6.5), ('兆易创新', '603986', 5.9),
            ('北方华创', '002371', 5.5), ('紫光国微', '002049', 5.2),
            ('三安光电', '600703', 4.8), ('圣邦股份', '300661', 4.5),
            ('长电科技', '600584', 4.2), ('中环股份', '002129', 3.8)
        ]
    },
    '019118': {  # 景顺长城纳斯达克科技市值加权 ETF 联接 (QDII)E
        'name': '景顺长城纳斯达克科技市值加权 ETF 联接 (QDII)E',
        'type': '纳斯达克科技',
        'holdings': [('纳斯达克科技', 'NQUSB', 95.0)]
    },
    '016708': {  # 华夏有色金属 ETF 联接 C
        'name': '华夏有色金属 ETF 联接 C',
        'type': '有色金属',
        'holdings': [
            ('紫金矿业', '601899', 8.5), ('洛阳钼业', '603993', 7.2),
            ('山东黄金', '600547', 6.8), ('中国铝业', '601600', 5.9),
            ('赣锋锂业', '002460', 5.5), ('天齐锂业', '002466', 5.2),
            ('北方稀土', '600111', 4.8), ('云南铜业', '000878', 4.5),
            ('中金黄金', '600489', 4.2), ('江西铜业', '600362', 3.8)
        ]
    },
    '006075': {  # 博时标普 500ETF 联接 (QDII)C
        'name': '博时标普 500ETF 联接 (QDII)C',
        'type': '标普 500',
        'holdings': [('标普 500', 'gb_SPX', 95.0)]
    },
    '020713': {  # 华安三菱日联日经 225ETF 联接 (QDII)C
        'name': '华安三菱日联日经 225ETF 联接 (QDII)C',
        'type': '日经 225',
        'holdings': [('日经 225', 'gb_N225', 95.0)]
    },
    '019305': {  # 摩根标普 500 指数 (QDII)C
        'name': '摩根标普 500 指数 (QDII)C',
        'type': '标普 500',
        'holdings': [('标普 500', 'gb_SPX', 95.0)]
    },
    '006105': {  # 宏利印度机会股票 (QDII)A
        'name': '宏利印度机会股票 (QDII)A',
        'type': '印度股票',
        'holdings': [('印度 50', 'gb_NIFTY', 90.0)]
    },
    '012979': {  # 大成恒生科技 ETF 联接 (QDII)A
        'name': '大成恒生科技 ETF 联接 (QDII)A',
        'type': '恒生科技',
        'holdings': [('恒生科技', 'hk_HSTECH', 95.0)]
    },
    '023828': {  # 万家中证半导体材料设备主题 ETF 联接 A
        'name': '万家中证半导体材料设备主题 ETF 联接 A',
        'type': '半导体',
        'holdings': [
            ('北方华创', '002371', 10.5), ('中微公司', '688012', 8.2),
            ('拓荆科技', '688072', 7.8), ('长川科技', '300604', 6.5),
            ('沪硅产业', '688126', 5.9), ('华海清科', '688120', 5.3),
            ('中科飞测', '688361', 4.8), ('南大光电', '300346', 4.2),
            ('安集科技', '688019', 3.9), ('芯源微', '688037', 3.7)
        ]
    }
}

def get_a_stock_price(code):
    """获取 A 股实时价格"""
    prefix = 'sz' if code.startswith('0') or code.startswith('3') else 'sh'
    url = f'http://qt.gtimg.cn/q={prefix}{code}'
    try:
        resp = session.get(url, timeout=5)
        resp.encoding = 'gbk'
        match = re.search(r'v_' + prefix + code + r'="([^"]+)"', resp.text)
        if match:
            parts = match.group(1).split('~')
            if len(parts) >= 32:
                current = float(parts[3]) if parts[3] else 0
                prev_close = float(parts[4]) if parts[4] else 0
                pct = float(parts[32]) if parts[32] else 0
                return current, pct
            elif len(parts) >= 6:
                current = float(parts[3]) if parts[3] else 0
                prev_close = float(parts[4]) if parts[4] else 0
                pct = float(parts[5]) if parts[5] else 0
                return current, pct
    except:
        pass
    return None, None

def get_global_index(ticker):
    """获取全球指数（使用腾讯财经）"""
    url = f'http://qt.gtimg.cn/q={ticker}'
    try:
        resp = session.get(url, timeout=10)
        resp.encoding = 'gbk'
        match = re.search(r'v_' + ticker + r'="([^"]+)"', resp.text)
        if match:
            parts = match.group(1).split('~')
            if len(parts) >= 6:
                current = float(parts[3]) if parts[3] else 0
                pct = float(parts[32]) if len(parts) > 32 and parts[32] else float(parts[5]) if parts[5] else 0
                return current, pct
    except:
        pass
    return None, None

def get_gold_price():
    """获取黄金价格（yfinance）"""
    try:
        import yfinance as yf
        t = yf.Ticker('GC=F')
        info = t.fast_info
        price = info.get('lastPrice', None)
        prev_close = info.get('previousClose', None)
        if price and prev_close:
            pct = (price - prev_close) / prev_close * 100
            return price, pct
    except:
        pass
    return None, None

def analyze_fund(fund_code, fund_info):
    """分析单支基金"""
    results = []
    total_weight = 0
    weighted_change = 0
    
    for stock_name, stock_code, weight in fund_info['holdings']:
        if stock_code in ['GC=F']:
            price, pct = get_gold_price()
        elif stock_code.startswith('gb_') or stock_code.startswith('hk_'):
            price, pct = get_global_index(stock_code)
        elif stock_code == '588000':  # 科创 50ETF
            price, pct = get_a_stock_price('588000')
        elif stock_code == 'CBA02701':  # 债券
            price, pct = 100.0, 0.01  # 债券波动极小
        else:
            price, pct = get_a_stock_price(stock_code)
        
        if pct is not None:
            total_weight += weight
            weighted_change += pct * weight
            arrow = 'UP' if pct > 0 else 'DOWN' if pct < 0 else 'FLAT'
            results.append((stock_name, price, pct, weight, arrow))
        else:
            results.append((stock_name, None, None, weight, 'NONE'))
    
    # 计算预估涨跌
    if total_weight > 0:
        avg_change = weighted_change / total_weight
        # ETF 联接基金通常 95% 仓位
        etf_weight = 0.95 if fund_info['type'] not in ['债券'] else 0.98
        estimated_change = avg_change * etf_weight
    else:
        estimated_change = 0
    
    return results, estimated_change

def main():
    print('=' * 80)
    print(f'持仓基金涨跌预估 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 80)
    print()
    
    # 读取持仓 CSV
    holdings = []
    try:
        with open('holdings.csv', 'r', encoding='gb18030') as f:
            reader = csv.DictReader(f)
            for row in reader:
                holdings.append(row)
    except Exception as e:
        print(f'无法读取 holdings.csv: {e}')
        print('使用默认配置')
    
    total_holdings = 0
    total_estimated_change = 0
    
    for fund_code, fund_info in FUND_HOLDINGS.items():
        # 查找持仓金额（CSV 列索引：0=名称，1=类型，2=代码，3=持有金额）
        holding_amount = 0
        for h in holdings:
            values = list(h.values())
            if len(values) >= 4:
                code = values[2]
                if str(code).strip() == fund_code:
                    try:
                        holding_amount = float(values[3])
                    except:
                        holding_amount = 0
                    break
        
        results, estimated_change = analyze_fund(fund_code, fund_info)
        
        arrow = 'UP' if estimated_change > 0 else 'DOWN' if estimated_change < 0 else 'FLAT'
        
        print('-' * 80)
        print(f"{fund_code} {fund_info['name']} ({fund_info['type']})")
        print(f"持仓金额：{holding_amount:,.2f} 元 | 预估涨跌：{arrow} {estimated_change:+.2f}%")
        print()
        
        # 显示前 5 大重仓股
        valid_results = [r for r in results if r[2] is not None]
        valid_results.sort(key=lambda x: abs(x[2]), reverse=True)
        
        print(f"{'股票':<12} {'价格':>10} {'涨跌%':>10} {'权重':>8}")
        print('-' * 45)
        for stock_name, price, pct, weight, arrow in valid_results[:5]:
            if price:
                print(f"{stock_name:<12} {price:>10.2f} {pct:>+10.2f}% {weight:>7.1f}%")
            else:
                print(f"{stock_name:<12} {'无数据':>10} {'--':>10} {weight:>7.1f}%")
        
        if holding_amount > 0:
            estimated_profit = holding_amount * (estimated_change / 100)
            total_holdings += holding_amount
            total_estimated_change += estimated_profit
            print()
            print(f"今日预估收益：{estimated_profit:+,.2f} 元")
        
        print()
    
    print('=' * 80)
    print('整体持仓预估')
    print('=' * 80)
    print(f"总持仓金额：{total_holdings:,.2f} 元")
    print(f"今日预估总收益：{total_estimated_change:+,.2f} 元")
    if total_holdings > 0:
        total_pct = (total_estimated_change / total_holdings) * 100
        print(f"整体涨跌幅：{total_pct:+.2f}%")
    print('=' * 80)

if __name__ == '__main__':
    main()
