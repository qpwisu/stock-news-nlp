import asyncio
import os
import re
from urllib.request import Request, urlopen
import time
import numpy as np
import aiohttp
from pykrx import stock
from datetime import date,datetime,timedelta
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from dateutil.relativedelta import relativedelta

# async를 쓰고 싶어도 스케줄러에 url을 넣고 돌려야하는데 그게 불가능 방법 모르겠음
# 검색어:종목명, 기간:1달, 최신순 정렬로 크롤링으로 네이버 뉴스 마지막 페이지 구하기
def crawling_stock_news_page(s_date,e_date): # 한달에 1시간 20분 걸리던걸 페이지 10개 미만 먼저 처리해서 15분만에 완료
    #오늘 코스피, 코스닥 상장 종목의 [티커,종목명] 리스트 구하기
    # today = date.today().strftime("%Y%m%d")
    day_list= []
    s_date =datetime.strptime(s_date,"%Y%m%d")
    e_date =datetime.strptime(e_date,"%Y%m%d")
    day_list.append(s_date.strftime("%Y.%m.%d"))
    while True:
      s_date += relativedelta(months=1)
      if e_date >= s_date:
          day_list.append(s_date.strftime("%Y.%m.%d"))
      else:
          if e_date != s_date:
              day_list.append(e_date.strftime("%Y.%m.%d"))
          break

    for i in range(len(day_list)-1):
        start_date = day_list[i]
        end_date = day_list[i+1]
        print(start_date)
        num_start_date = start_date.replace(".", "")
        num_end_date = end_date.replace(".", "")
        tickers = stock.get_market_ticker_list(num_end_date, market="KOSPI") + stock.get_market_ticker_list(
            num_end_date, market="KOSDAQ")
        company_list = []

        for ticker in tickers:
            name = stock.get_market_ticker_name(ticker)
            company_list.append([ticker, name, start_date, end_date])
        # 검색어:종목명, 기간:1달, 최신순 정렬로 크롤링으로 네이버 뉴스 마지막 페이지 구하기
        for i in tqdm(range(len(company_list))):
            # 페이지가 10개 미만이 것들은 먼저 처리
            url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={company}&sort=1&photo=3&field=0&pd=3&ds={sd}&de={ed}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{nsd}to{ned},a:all&start={page}' \
                .format(sd=start_date, ed=end_date, nsd=num_start_date, ned=num_end_date, company=company_list[i][1],
                        page=1)
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            page_list = [0]
            pages = soup.select('div.sc_page_inner a')

            for p in pages:
                page_list.append(int(p.text))
            if max(page_list) != 10:
                if max(page_list)==-1: # 뉴스가 없는 경우
                    continue
                company_list[i].append(max(page_list) - 1)
                continue

            min_page = 0
            max_page = 0
            tmp_page = 400
            while True:
                url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={company}&sort=1&photo=3&field=0&pd=3&ds={sd}&de={ed}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{nsd}to{ned},a:all&start={page}' \
                    .format(sd=start_date, ed=end_date, nsd=num_start_date, ned=num_end_date,
                            company=company_list[i][1], page=tmp_page * 10 + 1)
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.text, 'html.parser')
                news_titles = soup.select('.not_found02')  # 최대 페이지 이상인 경우 true
                # 400페이지가 최대임으로 400부터 절반씩 나눠가며 최대 페이지 찾음
                if news_titles:  # 최대페이지 이상인경우 값이 있음
                    max_page = tmp_page
                    tmp_page = min_page + int((max_page - min_page) / 2)
                    if max_page == tmp_page:
                        max_page = tmp_page
                        break
                else:
                    min_page = tmp_page
                    tmp_page = min_page + int((max_page - min_page) / 2)
                    if min_page == tmp_page:
                        max_page = tmp_page
                        break
            company_list[i].append(max_page)
        df = pd.DataFrame(company_list, columns=["ticker", "company_name", "start_date", "end_date", "max_page"])

        if not os.path.exists('max_page.csv'):
            df.to_csv('max_page.csv', index=False, mode='w', encoding='utf-8-sig')
        else:
            df.to_csv('max_page.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

# 0~ 마지막 페이지를 url로 생성
def get_url(s_date,e_date):
    tmp_li = []
    df = pd.read_csv("max_page.csv")
    start_date = datetime.strptime(s_date, "%Y%m%d").strftime("%Y.%m.%d")
    end_date = datetime.strptime(e_date, "%Y%m%d").strftime("%Y.%m.%d")
    df = df[(df["start_date"] >= start_date) & (df["end_date"] <= end_date)]

    for row in (df.itertuples()):
        ticker = getattr(row, "ticker")
        max_page =getattr(row, "max_page")
        max_page= int(max_page)
        if max_page==-1:
            continue
        start_date = getattr(row, "start_date")
        num_start_date = start_date.replace(".", "")
        end_date = getattr(row, "end_date")
        num_end_date = end_date.replace(".", "")
        company_name = getattr(row, "company_name")
        for page in range(0, max_page + 1):
            url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={company}&sort=1&photo=3&field=0&pd=3&ds={sd}&de={ed}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from{nsd}to{ned},a:all&start={page}' \
                .format(sd=start_date, ed=end_date, nsd=num_start_date, ned=num_end_date, company=company_name,
                        page=page * 10 + 1)
            tmp_li.append([ticker, company_name, start_date, end_date, max_page, url])
    url_df = pd.DataFrame(tmp_li, columns=["ticker", "company_name", "start_date", "end_date", "max_page", "url"])
    if not os.path.exists('max_page_url.csv'):
        url_df.to_csv('max_page_url.csv', index=False, mode='w', encoding='utf-8-sig')
    else:
        url_df.to_csv('max_page_url.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

# async를 사용하여 비동기로 url의 뉴스 타이틀,제공자,시간,링크 크롤링하기
# 네이버에서 크롤링 막음, colab으로 실행하면 잘됨
def async_crawling_news_title(s_date,e_date):

    async def main():
        df = pd.read_csv("max_page_url.csv")
        start_date = datetime.strptime(s_date, "%Y%m%d").strftime("%Y.%m.%d")
        end_date = datetime.strptime(e_date, "%Y%m%d").strftime("%Y.%m.%d")
        df = df[(df["start_date"] >= start_date) & (df["end_date"] <= end_date)]
        # df = df.iloc[np.random.permutation(df.index)].reset_index(drop=True)

        name_and_url_list = [[l, w] for l, w in zip(df["company_name"], df["url"])]
        # timeout error 해결 위해서 연결 시간 제한 x
        session_timeout = aiohttp.ClientTimeout(total=None)
        # connector = aiohttp.TCPConnector(limit=10)
        #connector = connector,timeout=session_timeout
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            input_coroutines = [get_news_url(session, li) for li in name_and_url_list]
            res = await asyncio.gather(*input_coroutines)

        res = sum(res, [])
        df = pd.DataFrame(res, columns=["company_name","title","provider","date","rink"])
        if not os.path.exists('news_crawling.csv'):
            df.to_csv('news_crawling.csv', index=False, mode='w', encoding='utf-8-sig')
        else:
            df.to_csv('news_crawling.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

    async def get_news_url(session,li):
        company_name = li[0]
        url = li[1]
        #두번째 오류 server_disconnect는 tcp 커넥터 제한이 있는거 같아서 50개로 제한걸어서 실행 해결 x
        # 프로그램이 아닌 크롬으로 직접 검색하는걸로 속이기 위함
        headers = {'User-Agent': 'Mozilla/5.0'}
        async with session.get(url,  headers=headers) as response:
            # 보안 관련 ssl오류가 떠서 체크 안하게 끔함 좋지 못한 방법 ssl=False
            try:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                news_list = soup.select('.list_news .news_wrap .news_area')
                if not news_list:
                    print(company_name,url)
                    print("err")
                    return []
                result  = []
                for news in news_list:
                    # extract news title
                    title = news.select_one('.news_tit').text.strip()
                    provider = news.select_one('.info_group a').text.strip()
                    date = news.select('.info_group span.info')[1].text.strip().replace(".","")
                    rink = news.select_one('.news_tit')['href']
                    result.append([company_name,title,provider,date,rink])
                # print(result)
                return result
            except:
                print(url)
                return []

    start = time.time()
    result = asyncio.run(main())
    end = time.time()
    print(f"{end - start:.5f} sec")

def crawling_news_title(s_date,e_date): #8만 페이지 4시간
    df = pd.read_csv("max_page_url.csv")
    start_date = datetime.strptime(s_date, "%Y%m%d").strftime("%Y.%m.%d")
    end_date = datetime.strptime(e_date, "%Y%m%d").strftime("%Y.%m.%d")
    df = df[(df["start_date"] >= start_date) & (df["end_date"] <= end_date)]

    name_and_url_list = [[l, w] for l, w in zip(df["company_name"], df["url"])]
    result = []
    for li in tqdm(name_and_url_list):
        company_name = li[0]
        url = li[1]
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.select('.list_news .news_wrap .news_area')
        if not news_list:
            print(company_name, url)
            print("err")
            return []
        for news in news_list:
            # extract news title
            title = news.select_one('.news_tit').text.strip()
            provider = news.select_one('.info_group a').text.strip()
            date = news.select('.info_group span.info')[1].text.strip().replace(".", "")
            if len(date)!=8:
                if "일 전" in date:
                    numbers = int(re.sub(r'[^0-9]', '', date))
                    date = (datetime.today() - timedelta(days=numbers)).strftime("%Y%m%d")
                elif "시간 전" in date:
                    numbers = int(re.sub(r'[^0-9]', '', date))
                    date = (datetime.today() - timedelta(minutes=numbers)).strftime("%Y%m%d")

            rink = news.select_one('.news_tit')['href']
            result.append([company_name, title, provider, date, rink])
    df = pd.DataFrame(result,columns=["company_name", "title", "provider", "date", "rink"])
    if not os.path.exists('news_crawling.csv'):
        df.to_csv('news_crawling.csv', index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('news_crawling.csv', index=False, mode='a', encoding='utf-8-sig', header=False)



# crawling_stock_news_page(start_date,end_date)
# get_url(start_date,end_date)
# async_crawling_news_title(start_date,end_date)
# crawling_news_title(start_date,end_date)

#1일 시작해서 1일을 끝으로 ex) 20220301, 20230301 -> 20220301~20230301
def crawling(start_date,end_date):
    crawling_stock_news_page(start_date,end_date)
    get_url(start_date,end_date)
    async_crawling_news_title(start_date,end_date)
    # crawling_news_title(start_date, end_date)
# start_date = "20230314"
# end_date = "20230321"
# crawling(start_date,end_date)


# 3만, 8만
df= pd.read_csv("news_crawling.csv")
# print(df.shape)
# print(df["title"].isnull().sum())
# print(df.iloc[-100:-1,1])
# df1 = pd.read_csv("max_page_url.csv").iloc[0:10000]
# print(df1["start_date"].max())
# print(df1.iloc[-1].url)
# df = pd.read_csv("news_crawling.csv")
# print(df.iloc[-1])

