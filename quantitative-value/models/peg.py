import pandas as pd
from common import *

def get_stocks(filepath, date, min_market_cap, max_market_cap, min_fund_rank, max_fund_rank, num_stocks, verbose=True):
    if verbose:
        print("------------------------------")
        print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})

    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'PER', '당기순이익-YoY']

    df = df[cols]
    if verbose:
        print('전체', len(df))

    # 국외주식 제외
    df = exclude_foreign_corps(df, '종목코드')
    if verbose:
        print('국외주식 제외', len(df))
    
#     # 유동비율 
#     df_qp = df_qp[df_qp['유동비율'] > 1.5]
#     if verbose:
#         print('유동비율', len(df_qp))
    
    df = df[df['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df = df.sort_values(by=['시가총액'])
    if verbose:
        print('가격정보 없는 기업 제외', len(df))
    df = df[int(len(df)*min_market_cap):int(len(df)*max_market_cap)]
    
    # 적자 기업 제외
    df = df[df['PER'] > 0]
    
    # get ranks
    df['PEG'] = df['PER'] / df['당기순이익-YoY']
    df['1/PEG'] = 1 / df['PEG']
    df['RANK_1'] = df['1/PEG'].rank(ascending=False)
    
    df['TOTAL_RANK'] = df['RANK_1']

    df = df.sort_values(by=['TOTAL_RANK'])    
    
    if len(df) > num_stocks:
        print(date, "선정 기업 수", num_stocks)
        return df['종목코드'].tolist()[:num_stocks]
    else:
        print(date, "선정 기업 수", len(df))
        return df['종목코드'].tolist()