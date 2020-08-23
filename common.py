BLACK_NAMES = ['보험', '화재', '금융', '홀딩스', '신용', '증권', '생명', '스팩']

def exclude_holdings_and_finances(df, col):    
    def corp_name_has_black(corp_name):
        for black_name in BLACK_NAMES:
            if black_name in corp_name:
                return True
        return False
        
    df['black'] = df.apply(lambda x: corp_name_has_black(x[col]), axis=1)
    df = df[df['black'] == False]
    return df

def exclude_foreign_corps(df, col):
    df['foreign'] = df.apply(lambda x: x[col][0] == '9', axis=1)
    df = df[df['foreign'] == False]
    return df

def exclude_minus_income_corps(df, cols):
    df['plus'] = True
    for col in cols:
        df[col] = df[col].fillna(0) # 당기순이익이 없는 경우 플러스로 만들기 위해 0으로 넣어줌
        df['plus'] = (df[col] >= 0) * df['plus']
    
    df = df[df['plus'] == True]
    return df