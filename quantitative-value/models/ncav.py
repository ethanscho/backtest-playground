import pandas as pd
from common import *

NUM_STOCKS = 30
NCAV = 1.0
LIQUID = 2.0

def get_stocks(filepath, date, verbose=True):
    print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})
    
    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'NCAV', '유동비율', '당기순이익', 'PER', 'PBR', 'GP/A']
    
    df_qp = df[cols]
    df_qp = df_qp[df_qp['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df_qp = df_qp[df_qp['PBR'] > 0]
    
    # 지주사, 금융사 제외
    df_qp = exclude_holdings_and_finances(df_qp, '회사명')
    
    # 국외주식 제외
    df_qp = exclude_foreign_corps(df_qp, '종목코드')

    # 청산비율 
    df_qp = df_qp[df_qp['NCAV'] > NCAV]
    df_qp = df_qp.sort_values(by=['NCAV'], ascending=False)

    # 유동비율
    df_qp = df_qp[df_qp['유동비율'] > LIQUID]
    
    # RANK
    df_qp['RANK_1'] = df_qp['NCAV'].rank(ascending=False)
    df_qp['TOTAL_RANK'] = df_qp['RANK_1'] #  + df_qp['RANK_2'] + df_qp['RANK_3']

    stocks = []
    counter = 0
    for i, row in df_qp.iterrows():
        counter += 1
        if counter > NUM_STOCKS:
            break
        
        candidate = row['종목코드']
        candidate_name = row['회사명']
            
        #print(candidate, candidate_name)
        stocks.append(candidate)
    
    print(len(stocks))
    return stocks