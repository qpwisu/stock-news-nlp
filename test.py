import pandas as pd
df = pd.read_csv("news_crawling.csv" )
df2 = pd.read_csv("p4_max_page3.csv",index_col=0)
df2 = df2.drop_duplicates(['title'])

df = pd.concat([df,df2])
df.to_csv("news.csv",index=False)

