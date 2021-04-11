import pandas as pd
from common import *

def get_stocks(filepath, date, min_market_cap, max_market_cap, min_fund_rank=None, max_fund_rank=None, num_stocks=30, verbose=True):
    if verbose:
        print("------------------------------")
        print(date, filepath)
    df = pd.read_csv(filepath, dtype={"기업코드":"string", "종목코드":"string"})
    
#     past_income_cols = []
#     last_year = int(date[:4]) - 1
#     for i in range(1, 6):
#         year = last_year - i
#         col_name = str(year) + '-' + '당기순이익'
#         past_income_cols.append(col_name)
        
    cols = ['종목코드', 'IFRS', 'CFS', '회사명', '시가총액', 'PBR', '영업이익', '자산총계', '유동비율']
    #cols.extend(past_income_cols)

    df = df[cols]
    if verbose:
        print('전체', len(df))
        
    df['OA'] = df['영업이익'] / df['자산총계']
    
    # 지주사, 금융사 제외
    df = exclude_holdings_and_finances(df, '회사명')
    if verbose:
        print('지주사, 금융사 제외', len(df))
    
    # 국외주식 제외
    df = exclude_foreign_corps(df, '종목코드')
    if verbose:
        print('국외주식 제외', len(df))
    
#     # 유동비율 > 150%
#     df = df[df['유동비율'] > 1.5]
#     if verbose:
#         print('유동비율 > 1.5', len(df))
        
#     # 주당배당금 > 0
#     df = df[df['주당배당금'] > 0.0]

#     # 전년도 증자 기업 제외
#     df_qp = df_qp[df_qp['증자'] == 0]
#     print('증자기업 제외', len(df_qp))

#     # 전년도 적자 기업 제외 
#     df_qp = df_qp[df_qp['당기순이익'] > 0]
#     print('당기순이익 적자 제외', len(df_qp))
    
#     # 전년도 영업현금흐름 적자 기업 제외 
#     df_qp = df_qp[df_qp['영업활동으로인한현금흐름'] > 0]
#     print('영업활동으로인한현금흐름 적자 제외', len(df_qp))
    
    # 당기순이익 최근 5년 +인것만
    #df_qp = exclude_minus_income_corps(df_qp, past_income_cols)

    # 시가총액 하위 20% 
    df = df[df['시가총액'] > 0] # 시가총액 data가 없는 row는 제거
    df = df.sort_values(by=['시가총액'])
    if verbose:
        print('가격정보 없는 기업 제외', len(df))
    df = df[int(len(df)*min_market_cap):int(len(df)*max_market_cap)]
    
    # get ranks
    df['1/PBR'] = 1 / df['PBR']
    df['RANK_1'] = df['1/PBR'].rank(ascending=False)
    
    df['RANK_2'] = df['OA'].rank(ascending=False) # 높을 수록 좋음
    
    df['TOTAL_RANK'] = df['RANK_1'] + df['RANK_2']

    df = df.sort_values(by=['TOTAL_RANK'])    
    
    if len(df) > num_stocks:
        print(date, "선정 기업 수", num_stocks)
        return df['종목코드'].tolist()[:num_stocks]
    else:
        print(date, "선정 기업 수", len(df))
        return df['종목코드'].tolist()