import pandas as pd
from common import *

def get_stocks(filepath, date, min_market_cap, max_market_cap, min_fund_rank, max_fund_rank, num_stocks, verbose=True):
    if verbose:
        print("------------------------------")
        print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})

    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'PBR', 'PCR', 'PER', 'PSR', '유동비율', '매출액(수익)-YoY']

    df_qp = df[cols]
    if verbose:
        print('전체', len(df_qp))

    # 국외주식 제외
    df_qp = exclude_foreign_corps(df_qp, '종목코드')
    if verbose:
        print('국외주식 제외', len(df_qp))
    
    df_qp = df_qp[df_qp['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df_qp = df_qp.sort_values(by=['시가총액'])
    if verbose:
        print('가격정보 없는 기업 제외', len(df_qp))
    df_qp = df_qp[int(len(df_qp)*min_market_cap):int(len(df_qp)*max_market_cap)]
    
    # get ranks
    df_qp = df_qp[df_qp['PSR'] > 0] # 적자 기업 제외
    df_qp = df_qp.sort_values(by=['PSR'])
    
    df_qp = df_qp[int(len(df_qp)*min_fund_rank):int(len(df_qp)*max_fund_rank)]
    
    # get ranks
    df['1/PSR'] = 1 / df['PSR']
    df['RANK_1'] = df['1/PSR'].rank(ascending=False)
    df['RANK_2'] = df['매출액(수익)-YoY'].rank(ascending=False) # 높을 수록 좋음
    
    df['TOTAL_RANK'] = df['RANK_1'] + df['RANK_2']

    df = df.sort_values(by=['TOTAL_RANK'])    
    
    if len(df_qp) > num_stocks:
        print(date, "선정 기업 수", num_stocks)
        return df_qp['종목코드'].tolist()[:num_stocks]
    else:
        print(date, "선정 기업 수", len(df_qp))
        return df_qp['종목코드'].tolist()