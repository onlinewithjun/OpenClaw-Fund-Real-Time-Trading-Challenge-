#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析 023828 基金持仓及预估涨跌
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import re

# 半导体设备 ETF 重仓股（根据最新季报）
# 023828 是 ETF 联接基金，跟踪半导体设备 ETF(159327)
stocks = [
    ('北方华创', '002371', 10.5),
    ('中微公司', '688012', 8.2),
    ('拓荆科技', '688072', 7.8),
    ('长川科技', '300604', 6.5),
    ('沪硅产业', '688126', 5.9),
    ('华海清科', '688120', 5.3),
    ('中科飞测', '688361', 4.8),
    ('南大光电', '300346', 4.2),
    ('安集科技', '688019', 3.9),
    ('芯源微', '688037', 3.7),
]

session = requests.Session()
session.trust_env = False

codes = ','.join([f'sz{code}' if code.startswith('0') or code.startswith('3') else f'sh{code}' for _, code, _ in stocks])
url = f'http://qt.gtimg.cn/q={codes}'

resp = session.get(url, timeout=10)
resp.encoding = 'gbk'
text = resp.text

print('=' * 70)
print('023828 万家中证半导体材料设备 ETF 联接 A - 持仓分析')
print('=' * 70)
print()

total_weight = 0
weighted_change = 0

print('【前十大重仓股实时行情】')
print()

for name, code, weight in stocks:
    prefix = 'sz' if code.startswith('0') or code.startswith('3') else 'sh'
    pattern = r'v_' + prefix + code + r'="([^"]+)"'
    match = re.search(pattern, text)
    
    if match:
        parts = match.group(1).split('~')
        if len(parts) >= 32:
            # 腾讯 API 格式：v_shXXXXXX="51~名称~代码~当前价~昨收~涨跌额~涨跌幅~..."
            # 涨跌幅在索引 32
            current = float(parts[3]) if parts[3] else 0
            prev_close = float(parts[4]) if parts[4] else 0
            pct = float(parts[32]) if len(parts) > 32 and parts[32] else 0
            change = current - prev_close
            
            arrow = 'UP' if pct > 0 else 'DOWN' if pct < 0 else 'FLAT'
            print(f'{arrow} {name} ({code}): {current:.2f} ({change:+.2f}, {pct:+.2f}%) [权重:{weight}%]')
            
            total_weight += weight
            weighted_change += pct * weight
        elif len(parts) >= 6:
            # 备用解析
            current = float(parts[3]) if parts[3] else 0
            prev_close = float(parts[4]) if parts[4] else 0
            pct = float(parts[5]) if parts[5] else 0
            change = current - prev_close
            
            arrow = 'UP' if pct > 0 else 'DOWN' if pct < 0 else 'FLAT'
            print(f'{arrow} {name} ({code}): {current:.2f} ({change:+.2f}, {pct:+.2f}%) [权重:{weight}%]')
            
            total_weight += weight
            weighted_change += pct * weight
        else:
            print(f'FLAT {name} ({code}): 数据格式错误')
    else:
        print(f'FLAT {name} ({code}): 无数据')

print()
print('=' * 70)
print('【基金涨跌预估】')
print()

if total_weight > 0:
    estimated_change = weighted_change / total_weight
    etf_weight = 0.95
    estimated_fund_change = estimated_change * etf_weight
    
    arrow = 'UP' if estimated_fund_change > 0 else 'DOWN' if estimated_fund_change < 0 else 'FLAT'
    
    print(f'重仓股平均涨跌：{estimated_change:+.2f}%')
    print(f'ETF 仓位比例：约 {etf_weight*100:.0f}%')
    print()
    print(f'{arrow} 预估基金涨跌：{estimated_fund_change:+.2f}%')
    print()
    print('注：预估基于前十大重仓股（占总持仓约 60%），实际涨跌可能有偏差')
else:
    print('无法计算，数据获取失败')

print()
print('=' * 70)
print('【基金档案】')
print()
print('基金代码：023828')
print('基金名称：万家中证半导体材料设备主题 ETF 发起式联接 A')
print('跟踪指数：中证半导体材料设备主题指数')
print('基金类型：ETF 联接基金（股票型，中高风险）')
print('成立时间：2025 年 4 月 29 日')
print('基金公司：万家基金管理有限公司')
print()
print('持仓特点：')
print('- 主要投资于半导体材料和设备行业')
print('- 重仓股集中在刻蚀机、薄膜沉积、清洗设备等设备厂商')
print('- 受半导体周期、国产替代政策影响较大')
print('=' * 70)
