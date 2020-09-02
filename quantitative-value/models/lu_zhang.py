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
    
    past_asset_cols = []
    last_year = int(date[:4]) - 1
    for i in range(1, 6):
        year = last_year - i
        col_name = str(year) + '-' + '자본총계'
        past_asset_cols.append(col_name)
        
    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'ROE', '자본총계']
    cols.extend(past_asset_cols)

    df = df[cols]
    if verbose:
        print('전체', len(df))
    
    # 지주사, 금융사 제외
    df = exclude_holdings_and_finances(df, '회사명')
    if verbose:
        print('지주사, 금융사 제외', len(df))
    
    # 국외주식 제외
    df = exclude_foreign_corps(df, '종목코드')
    if verbose:
        print('국외주식 제외', len(df))
    
    # 자산성장률
    df['자본성장률'] = (df['자본총계'] - df[past_asset_cols[0]]) / df[past_asset_cols[0]]

    # 시가총액
    df = df[df['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df = df.sort_values(by=['시가총액'])
    df = df[int(len(df)*MIN_MARKET_CAP):int(len(df)*MAX_MARKET_CAP)]
    
    # get ranks
    df['1/자본성장률'] = 1 / df['자본성장률']
    df['RANK_1'] = df['1/자본성장률'].rank(ascending=False)
    df['RANK_2'] = df['ROE'].rank(ascending=False)
    
    df['TOTAL_RANK'] = df['RANK_1'] + df['RANK_2']

    df = df.sort_values(by=['TOTAL_RANK'])    
    
    stocks = []
    counter = 0
    for i, row in df.iterrows():
        counter += 1
        if counter > NUM_STOCKS:
            break
        
        candidate = row['종목코드']
        candidate_name = row['회사명']
            
        #print(candidate_name, row['TOTAL_RANK'])
        stocks.append(candidate)
    
    if verbose:
        print("선정 기업 수", len(stocks))
    else:
        print(date, "선정 기업 수", len(stocks))
    return stocks