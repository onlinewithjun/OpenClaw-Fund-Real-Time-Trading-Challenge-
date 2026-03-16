# -*- coding: utf-8 -*-
"""
基金实盘收益更新 - 2026 年 3 月 6 日
查询持仓基金今日净值，计算当日盈亏和累计盈亏
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 基金持仓数据 (从 memory/2026-03-03.md 提取)
holdings = [
    {"name": "易方达黄金 ETF 联接 C", "type": "黄金", "code": "002963", "holding": 61118.93, "cum_profit": 26118.93},
    {"name": "景顺长城科创 50 联接 C", "type": "科创 50", "code": "021485", "holding": 52242.05, "cum_profit": 13241.91},
    {"name": "摩根日本精选股票 (QDII)C", "type": "日本股票", "code": "019449", "holding": 49673.65, "cum_profit": 10773.65},
    {"name": "易方达人工智能 ETF 联接 A", "type": "人工智能", "code": "012733", "holding": 44021.07, "cum_profit": 8021.07},
    {"name": "华夏科创 50ETF 联接 A", "type": "科创 50", "code": "011612", "holding": 30973.73, "cum_profit": 6973.73},
    {"name": "华安黄金 ETF 联接 C", "type": "黄金", "code": "000217", "holding": 31642.07, "cum_profit": 6642.07},
    {"name": "广发纳斯达克 100ETF 联接 (QDII)C", "type": "纳斯达克", "code": "006479", "holding": 47947.78, "cum_profit": 6287.78},
    {"name": "广发中债 7-10 年期国开行债券指数 A", "type": "债券", "code": "003376", "holding": 100971.84, "cum_profit": 5555.34},
    {"name": "华夏国证半导体芯片 ETF 联接 A", "type": "半导体", "code": "008887", "holding": 23217.39, "cum_profit": 3217.39},
    {"name": "景顺长城纳斯达克科技市值加权 ETF 联接 (QDII)E", "type": "纳斯达克科技", "code": "019118", "holding": 26932.07, "cum_profit": 1432.07},
    {"name": "华夏有色金属 ETF 联接 C", "type": "有色金属", "code": "016708", "holding": 10429.50, "cum_profit": 429.50},
    {"name": "7 日理财+", "type": "理财", "code": "N/A", "holding": 96196.46, "cum_profit": 196.46},
    {"name": "博时标普 500ETF 联接 (QDII)C", "type": "标普 500", "code": "006075", "holding": 1177.45, "cum_profit": 177.45},
    {"name": "华安三菱日联日经 225ETF 联接 (QDII)C", "type": "日经 225", "code": "020713", "holding": 1600.28, "cum_profit": 130.28},
    {"name": "摩根标普 500 指数 (QDII)C", "type": "标普 500", "code": "019305", "holding": 497.58, "cum_profit": -2.42},
    {"name": "宏利印度机会股票 (QDII)A", "type": "印度股票", "code": "006105", "holding": 886.70, "cum_profit": -113.30},
    {"name": "大成恒生科技 ETF 联接 (QDII)A", "type": "恒生科技", "code": "012979", "holding": 9754.63, "cum_profit": -245.37},
    {"name": "万家中证半导体材料设备主题 ETF 联接 A", "type": "半导体", "code": "023828", "holding": 19632.27, "cum_profit": -367.73},
]

# 今天是 2026 年 3 月 6 日 (周五)
today = "20260306"
yesterday = "20260305"  # 周四

print(f"基金实盘收益更新 - {today}")
print("=" * 60)

results = []

for fund in holdings:
    if fund["code"] == "N/A":
        # 理财产品，假设每日固定收益
        daily_profit = fund["holding"] * 0.0002  # 假设年化 2%
        results.append({
            **fund,
            "today_nav": "N/A",
            "yesterday_nav": "N/A",
            "change_pct": 0.02,
            "daily_profit": daily_profit,
            "new_cum_profit": fund["cum_profit"] + daily_profit
        })
        continue
    
    try:
        # 获取基金历史净值数据
        df = ak.fund_open_fund_info_em(symbol=fund["code"], indicator="单位净值走势")
        
        if df is None or len(df) == 0:
            print(f"⚠️  {fund['code']} - 无数据")
            continue
        
        # 获取最近两天的净值
        df = df.head(2)
        
        if len(df) < 2:
            # 只有一天数据，使用最新净值
            today_nav = float(df.iloc[0]["单位净值"])
            yesterday_nav = today_nav
            change_pct = 0
        else:
            today_nav = float(df.iloc[0]["单位净值"])
            yesterday_nav = float(df.iloc[1]["单位净值"])
            change_pct = ((today_nav - yesterday_nav) / yesterday_nav) * 100
        
        # 计算当日盈亏
        # 持仓金额 = 份额 * 今日净值
        # 份额 = 持仓金额 / (今日净值 * (1 - 累计收益率/100))
        # 简化计算：当日盈亏 = 持仓金额 * 涨跌幅%
        daily_profit = fund["holding"] * (change_pct / 100)
        new_cum_profit = fund["cum_profit"] + daily_profit
        
        results.append({
            **fund,
            "today_nav": today_nav,
            "yesterday_nav": yesterday_nav,
            "change_pct": change_pct,
            "daily_profit": daily_profit,
            "new_cum_profit": new_cum_profit
        })
        
        print(f"[OK] {fund['code']} - {fund['name']}: {change_pct:+.2f}%, 当日盈亏：{daily_profit:+.2f}元")
        
    except Exception as e:
        print(f"[ERR] {fund['code']} - Error: {str(e)}")
        results.append({
            **fund,
            "today_nav": "Error",
            "yesterday_nav": "Error",
            "change_pct": 0,
            "daily_profit": 0,
            "new_cum_profit": fund["cum_profit"]
        })

# 汇总统计
total_holding = sum(r["holding"] for r in results)
total_daily_profit = sum(r["daily_profit"] for r in results)
total_cum_profit = sum(r["new_cum_profit"] for r in results)

print("\n" + "=" * 60)
print(f"汇总统计:")
print(f"  总持仓：{total_holding:,.2f} 元")
print(f"  当日盈亏：{total_daily_profit:+,.2f} 元")
print(f"  累计盈亏：{total_cum_profit:+,.2f} 元")
print(f"  累计收益率：{(total_cum_profit/total_holding)*100:+.2f}%")

# 保存结果到 CSV
results_df = pd.DataFrame(results)
results_df.to_csv("C:/Users/Administrator/.openclaw/workspace/fund_results_20260306.csv", index=False, encoding='utf-8-sig')
print(f"\n结果已保存到：fund_results_20260306.csv")
