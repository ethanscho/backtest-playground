import pandas as pd
from common import *

NUM_STOCKS = 30
MIN_MARKET_CAP = 0.0
MAX_MARKET_CAP = 0.2

def get_stocks(filepath, date, verbose=True):
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
    df_qp = df_qp[int(len(df_qp)*MIN_MARKET_CAP):int(len(df_qp)*MAX_MARKET_CAP)]
    
    # get ranks
    df_qp['1/PBR'] = 1 / df_qp['PBR']
#     df_qp['1/PCR'] = 1 / df_qp['PCR']
#     df_qp['1/PER'] = 1 / df_qp['PER']
    df_qp['1/PSR'] = 1 / df_qp['PSR']
    
    df_qp['RANK_1'] = df_qp['1/PBR'].rank(ascending=False)
#     df_qp['RANK_2'] = df_qp['1/PCR'].rank(ascending=False)
#     df_qp['RANK_3'] = df_qp['1/PER'].rank(ascending=False)
    df_qp['RANK_2'] = df_qp['1/PSR'].rank(ascending=False)
    
    df_qp['TOTAL_RANK'] = df_qp['RANK_1'] + df_qp['RANK_2'] # + df_qp['RANK_3'] + df_qp['RANK_4']

    df_qp = df_qp.sort_values(by=['TOTAL_RANK'])    
    
    stocks = []
    counter = 0
    for i, row in df_qp.iterrows():
        counter += 1
        if counter > NUM_STOCKS:
            break
        
        candidate = row['종목코드']
        candidate_name = row['회사명']
            
        #print(candidate_name, row['TOTAL_RANK'])
        stocks.append(candidate)
    
    print(date, "선정 기업 수", len(stocks))
    return stocks