"""
고유 명사 추가하기 mecab-ko-dic
위치 : /Users/janghan-yeong/opt/anaconda3/envs/news_crawling/lib/python3.7/site-packages/mecab-ko-dic-2.1.1-20180720
참고 사이트 : https://heytech.tistory.com/15

1. cd user-dic
2. vi nnp.csv
3. 고유명상,,,,NNP,*,T,고유명상,*,*,*,*,*
    - 빈칸있음 오류뜸
4. cd .. | cd tools
5. sh add-userdic.sh |  cd .. | make install

"""
from datetime import datetime

from pykrx import stock
import pandas as pd
noun_dic_location = "/Users/janghan-yeong/opt/anaconda3/envs/news_crawling" \
                    "/lib/python3.7/site-packages/mecab-ko-dic-2.1.1-20180720"\
                    "/user-dic/nnp.csv"
noun_dic = pd.read_csv(noun_dic_location,header=None)
print(noun_dic)

today = datetime.today()
tickers = stock.get_market_ticker_list(today, market="KOSPI") + stock.get_market_ticker_list(
    today, market="KOSDAQ")
company_list = []

for ticker in tickers:
    name = stock.get_market_ticker_name(ticker)
    company_list.append(name)

df = pd.DataFrame(columns=[0,1,2,3,4,5,6,7,8,9,10,11,12])
df[0]= company_list
df[7]= company_list
df[4]= "NNP"
df[6]= "T"
df[5]= "*"
df[8]= "*"
df[9]= "*"
df[10]= "*"
df[11]= "*"
df[12]= "*"

print(len(company_list))
# df.to_csv(noun_dic_location,mode="a",header=None,index=None)
