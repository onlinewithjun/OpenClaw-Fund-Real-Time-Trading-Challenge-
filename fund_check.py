import akshare as ak
import pandas as pd

# 获取基金实时估值
fund_codes = ['020899', '017192', '002611']
print('=== 基金实时估值 ===')
for code in fund_codes:
    try:
        df = ak.fund_etf_fund_info_em(fund=code)
        print(f'{code}:')
        print(df)
        print()
    except Exception as e:
        print(f'{code}: 获取失败 - {e}')
