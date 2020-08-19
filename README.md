# Backtest playground

## Setup
```
git clone https://github.com/ethanscho/backtest-playground.git
cd backtest-playground
git clone https://github.com/FinanceData/marcap.git
```

## Models
### GP/A + 1/PBR 
- 시총하위 20%
- 상위 종목 30개 
- 1년에 1번, 매년 8/1 리밸런싱
- CAGR: 45.48%

```
run backtest.ipynb 
```

### NCAV
- 유동비율 (유동자산/유동부채) > 2.0
- 청산비율 ((유동자산 - 총부채) / 가격) > 1.0
- 청산비율 상위 종목 30개 
- 1년에 1번, 매년 8/1 리밸런싱
- CAGR: 23.13%

```
run backtest.ipynb 
```

### PBR + PCR + PER + PSR
- 시총하위 20%
- 상위 종목 30개 
- 유동비율 100% 이상
- 1년에 1번, 매년 8/1 리밸런싱
- CAGR: 32.42%

```
run backtest.ipynb 
```

