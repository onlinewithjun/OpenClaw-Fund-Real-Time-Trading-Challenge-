#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时行情获取脚本 - 新浪财经 API
"""

import requests
import re
from datetime import datetime

def get_china_indices():
    """获取 A 股指数（新浪财经 API）"""
    # 上证指数 s_sh000001, 深证成指 sz399001, 科创 50 sh000688, 创业板指 sz399006
    symbols = [
        ('上证指数', 'sh000001'),
        ('深证成指', 'sz399001'),
        ('科创 50', 'sh000688'),
        ('创业板指', 'sz399006'),
        ('沪深 300', 'sh000300')
    ]
    
    results = []
    for name, symbol in symbols:
        try:
            url = f"http://hq.sinajs.cn/list={symbol}"
            resp = requests.get(url, timeout=5)
            resp.encoding = 'gbk'
            text = resp.text
            
            # 解析：var hq_str_sh000001="名称，开盘，昨收，当前，最高，最低，..."
            match = re.search(r'"([^"]+)"', text)
            if match:
                parts = match.group(1).split(',')
                if len(parts) >= 4:
                    current = float(parts[3]) if parts[3] else 0
                    prev_close = float(parts[2]) if parts[2] else 0
                    change = current - prev_close
                    pct = (change / prev_close * 100) if prev_close else 0
                    results.append(f"{name}: {current:.2f} ({change:+.2f}, {pct:+.2f}%)")
                else:
                    results.append(f"{name}: 数据格式错误")
            else:
                results.append(f"{name}: 无数据")
        except Exception as e:
            results.append(f"{name}: 错误")
    
    return results

def get_funds_nav():
    """获取基金净值（天天基金 API）"""
    fund_codes = [
        ('002963', '易方达黄金'),
        ('021485', '景顺科创 50'),
        ('019449', '摩根日本'),
        ('012733', '易方达 AI'),
        ('011612', '华夏科创 50'),
        ('000217', '华安黄金'),
        ('006479', '广发纳指 100'),
        ('003376', '广发债券'),
        ('008887', '华夏芯片'),
        ('019118', '景顺纳指科技'),
        ('016708', '华夏有色'),
        ('006075', '博时标普 500'),
        ('020713', '华安日经 225'),
        ('019305', '摩根标普 500'),
        ('006105', '宏利印度'),
        ('012979', '大成恒生科技'),
        ('023828', '万家半导体')
    ]
    
    results = []
    for code, short_name in fund_codes:
        try:
            url = f"http://fund.eastmoney.com/pingzhongdata/{code}.js"
            resp = requests.get(url, timeout=5)
            resp.encoding = 'utf-8'
            text = resp.text
            
            # 查找 unitMoney 字段
            match = re.search(r'unitMoney\s*=\s*\[([^\]]+)\]', text)
            if match:
                # 最新净值数据
                nav_data = match.group(1).split(',')
                if len(nav_data) >= 2:
                    date_str = nav_data[0].strip('"')
                    nav = float(nav_data[1]) if nav_data[1] else 0
                    # 查找日增长率
                    zzl_match = re.search(r'grateData\s*=\s*\[([^\]]+)\]', text)
                    zzl = 'N/A'
                    if zzl_match:
                        zzl_data = zzl_match.group(1).split(',')
                        if zzl_data[0]:
                            zzl = f"{float(zzl_data[0]):.2f}"
                    results.append(f"{code} {short_name}: {nav:.4f} ({zzl}%) [{date_str}]")
                else:
                    results.append(f"{code} {short_name}: 无数据")
            else:
                results.append(f"{code} {short_name}: 无数据")
        except Exception as e:
            results.append(f"{code} {short_name}: 错误")
    
    return results

def main():
    print("=" * 60)
    print(f"实时行情数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    print("\n【A 股指数】")
    for line in get_china_indices():
        print(line)
    
    print("\n【基金净值】(最新交易日)")
    for line in get_funds_nav():
        print(line)
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
