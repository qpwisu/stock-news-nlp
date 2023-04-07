import pandas as pd
df = pd.read_csv("news_word_embedding/dataFile/news.csv" )
n = 0
print(df.shape)
for i,r in df.iterrows():
    n+=len(r["title"].split())
print(n)