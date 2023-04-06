# Load and test embedding model
# model_name = 'word2vec-kowiki.model'	# Word2Vec model
# C> wv_test.py 'word2vec-kowiki.model'
import pandas as pd
from pykrx import stock
from gensim.models import Word2Vec
import sys
from datetime import datetime

def search_relation_stock(model,company_name):
    today = datetime.today()
    tickers = stock.get_market_ticker_list(today, market="KOSPI") + stock.get_market_ticker_list(
        today, market="KOSDAQ")
    company_list = []

    for ticker in tickers:
        name = stock.get_market_ticker_name(ticker)
        company_list.append(name)
    stock_df = pd.DataFrame(columns=["company_name","similarity"])
    stock_df["company_name"] = company_list

    for i in stock_df.index:
        try:
            stock_df.iloc[i,1] = model.wv.similarity(u'{0}'.format(company_name), u'{0}'.format(stock_df.iloc[i,0]))
        except:
            stock_df.iloc[i,1] = -99

    print(stock_df.sort_values("similarity",ascending=False).head(5))
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("C> wv_test.py word2vec.model")
    #     exit()
    # print("\nLoading Korean word embedding vectors for 'KMA tokenized text file'.\n")
    # model_name = sys.argv[1]  # Word2Vec model -- 'word2vec-kowiki.model'
    model_name = "word2vec-news_mecab.model"

    model = Word2Vec.load(model_name)

    # print(model.wv.get_vector(u'배우'))
    # print(model.wv.get_vector(u'여배우'))
    #
    # print(model.wv.similarity(u'LG', u'SK하이닉스'))
    # print(model.wv.similarity(u'카카오', u'카카오뱅크'))
    # print(model.wv.similarity(u'카카오페이', u'카카오뱅크'))
    # print(model.wv.similarity(u'카카오', u'삼성전자'))
    # print(model.wv.similarity(u'현대차', u'기아'))
    print("한미약품 관련 종목")
    search_relation_stock(model,"한미약품")
    # search_relation_stock(model,"반도체")



    # print(model.wv.similarity(u'배우', u'남자'))
    # print(model.wv.similarity(u'남자', u'여배우'))

    # print(model.wv.most_similar(positive=[u'카카오'], topn=3))
    # print(model.wv.most_similar(positive=[u'현대차', u'기아'],  topn=3))
    # print(model.wv.most_similar(positive=[u'현대차', u'기아'], negative=[u'카카오'], topn=3))
