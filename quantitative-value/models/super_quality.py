import pandas as pd
from common import *

NUM_STOCKS = 30
MIN_MARKET_CAP = 0.0
MAX_MARKET_CAP = 0.2

def get_stocks(filepath, date, verbose=True):
    print("------------------------------")
    print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})

    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'GP/A', '당기순이익', '증자', '영업활동으로인한현금흐름']
    #cols.extend(past_income_cols)

    df_qp = df[cols]
    print('전체', len(df_qp))
    
    # 지주사, 금융사 제외
    df_qp = exclude_holdings_and_finances(df_qp, '회사명')
    print('지주사, 금융사 제외', len(df_qp))
    
    # 국외주식 제외
    df_qp = exclude_foreign_corps(df_qp, '종목코드')
    print('국외주식 제외', len(df_qp))
    
    # 전년도 증자 기업 제외
    df_qp = df_qp[df_qp['증자'] == 0]
    print('증자기업 제외', len(df_qp))

    # 전년도 적자 기업 제외 
    df_qp = df_qp[df_qp['당기순이익'] > 0]
    print('당기순이익 적자 제외', len(df_qp))
    
    # 전년도 영업현금흐름 적자 기업 제외 
    df_qp = df_qp[df_qp['영업활동으로인한현금흐름'] > 0]
    print('영업활동으로인한현금흐름 적자 제외', len(df_qp))
    
    # 시가총액 하위 20% 
    df_qp = df_qp[df_qp['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df_qp = df_qp.sort_values(by=['시가총액'])
    print('가격정보 없는 기업 제외', len(df_qp))
    df_qp = df_qp[int(len(df_qp)*MIN_MARKET_CAP):int(len(df_qp)*MAX_MARKET_CAP)]
    
    # get ranks
    df_qp['RANK'] = df_qp['GP/A'].rank(ascending=False)
    df_qp = df_qp.sort_values(by=['RANK'])
    
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
    
    print("선정 기업 수", len(stocks))
    return stocks