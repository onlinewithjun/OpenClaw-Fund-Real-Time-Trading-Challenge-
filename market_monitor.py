#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时行情监控脚本 - 腾讯财经 API
解决代理和防火墙问题
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import requests
import re
import pandas as pd
from datetime import datetime

# 配置代理：国内 API 直连，国外 API 走代理
# 腾讯财经 API 不走代理
session_cn = requests.Session()
session_cn.trust_env = False  # 忽略系统代理，直连国内 API

# 国外 API 使用系统代理（Clash）
session_global = requests.Session()
session_global.trust_env = True  # 使用系统代理

def get_china_indices():
    """获取 A 股指数（腾讯财经 API）"""
    indices = [
        ('上证指数', 'sh000001'),
        ('深证成指', 'sz399001'),
        ('科创 50', 'sh000688'),
        ('创业板指', 'sz399006'),
        ('沪深 300', 'sh000300')
    ]
    
    results = []
    
    # 批量查询
    codes = ','.join([code for _, code in indices])
    url = f"http://qt.gtimg.cn/q={codes}"
    
    try:
        resp = session_cn.get(url, timeout=10)
        resp.encoding = 'gbk'
        text = resp.text
        
        for name, code in indices:
            try:
                # 解析：v_sh000001="51~上证指数~000001~4180.46~..."
                pattern = rf'v_{code}="([^"]+)"'
                match = re.search(pattern, text)
                
                if match:
                    parts = match.group(1).split('~')
                    if len(parts) >= 5:
                        # parts[3]=当前价，parts[4]=昨收，parts[32]=涨跌幅
                        current = float(parts[3]) if parts[3] else 0
                        prev_close = float(parts[4]) if parts[4] else 0
                        # 涨跌幅百分比在 parts[32]
                        pct_str = parts[32] if len(parts) > 32 else parts[5]
                        pct = float(pct_str) if pct_str else 0
                        change = current - prev_close
                        
                        results.append({
                            '名称': name,
                            '最新价': round(current, 2),
                            '涨跌额': round(change, 2),
                            '涨跌幅 (%)': round(pct, 2)
                        })
                    else:
                        results.append({'名称': name, '最新价': 0, '涨跌额': 0, '涨跌幅 (%)': 0})
                else:
                    results.append({'名称': name, '最新价': 0, '涨跌额': 0, '涨跌幅 (%)': 0})
            except Exception as e:
                results.append({'名称': name, '最新价': 0, '涨跌额': 0, '涨跌幅 (%)': 0})
                
    except Exception as e:
        for name, _ in indices:
            results.append({'名称': name, '最新价': 0, '涨跌额': 0, '涨跌幅 (%)': 0})
    
    return pd.DataFrame(results)

def get_global_markets():
    """获取全球市场（yfinance + 系统代理）"""
    try:
        import yfinance as yf
        tickers = {
            '黄金': 'GC=F',
            '原油': 'CL=F',
            '标普 500': '^GSPC',
            '纳斯达克': '^IXIC',
            '日经 225': '^N225',
            '恒生指数': '^HSI'
        }
        
        results = []
        for name, ticker in tickers.items():
            try:
                t = yf.Ticker(ticker)
                # 使用 fast_info 获取实时价格
                info = t.fast_info
                price = info.get('lastPrice', None)
                prev_close = info.get('previousClose', None)
                
                if price and prev_close:
                    change = price - prev_close
                    pct = (change / prev_close * 100) if prev_close else 0
                    results.append(f"{name}: {price:.2f} ({change:+.2f}, {pct:+.2f}%)")
                else:
                    # 回退到历史数据
                    hist = t.history(period='2d', timeout=15)
                    if len(hist) >= 2:
                        price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2]
                        change = price - prev_close
                        pct = (change / prev_close * 100) if prev_close else 0
                        results.append(f"{name}: {price:.2f} ({change:+.2f}, {pct:+.2f}%)")
                    else:
                        results.append(f"{name}: 无数据")
            except Exception as e:
                results.append(f"{name}: 无数据")
        
        return results
    except Exception as e:
        return [f'全球市场：{e}']

def main():
    print("=" * 70)
    print(f"实时行情监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    print("\n【A 股指数】")
    china_df = get_china_indices()
    for _, row in china_df.iterrows():
        pct = row['涨跌幅 (%)']
        if row['最新价'] > 0:
            arrow = '📈' if pct > 0 else '📉' if pct < 0 else '➖'
            print(f"{arrow} {row['名称']}: {row['最新价']:.2f} ({row['涨跌额']:+.2f}, {pct:+.2f}%)")
        else:
            print(f"➖ {row['名称']}: 数据获取失败")
    
    print("\n【全球市场】")
    for line in get_global_markets():
        print(line)
    
    print("\n" + "=" * 70)
    print("注：基金净值数据需等待交易日晚上更新")
    print("=" * 70)

if __name__ == '__main__':
    main()
