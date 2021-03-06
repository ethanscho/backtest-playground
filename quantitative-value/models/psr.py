import pandas as pd
from common import *

def get_stocks(filepath, date, min_market_cap, max_market_cap, min_fund_rank, max_fund_rank, num_stocks, verbose=True):
    if verbose:
        print("------------------------------")
        print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})

    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'PBR', 'PCR', 'PER', 'PSR', '유동비율']

    df_qp = df[cols]
    if verbose:
        print('전체', len(df_qp))
    
#     # 지주사, 금융사 제외
#     df_qp = exclude_holdings_and_finances(df_qp, '회사명')
#     if verbose:
#         print('지주사, 금융사 제외', len(df_qp))
    
    # 국외주식 제외
    df_qp = exclude_foreign_corps(df_qp, '종목코드')
    if verbose:
        print('국외주식 제외', len(df_qp))
    
#     # 유동비율 
#     df_qp = df_qp[df_qp['유동비율'] > 1.5]
#     if verbose:
#         print('유동비율', len(df_qp))
    
    # 시가총액 하위 20% 
    df_qp = df_qp[df_qp['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df_qp = df_qp.sort_values(by=['시가총액'])
    if verbose:
        print('가격정보 없는 기업 제외', len(df_qp))
    df_qp = df_qp[int(len(df_qp)*min_market_cap):int(len(df_qp)*max_market_cap)]
    
    if verbose:
        print(len(df_qp))
    
    # get ranks
    df_qp = df_qp[df_qp['PSR'] > 0]
    df_qp = df_qp.sort_values(by=['PSR'])
    
    df_qp = df_qp[int(len(df_qp)*min_fund_rank):int(len(df_qp)*max_fund_rank)]
    
    if len(df_qp) > num_stocks:
        print(date, "선정 기업 수", num_stocks)
        return df_qp['종목코드'].tolist()[:num_stocks]
    else:
        print(date, "선정 기업 수", len(df_qp))
        return df_qp['종목코드'].tolist()