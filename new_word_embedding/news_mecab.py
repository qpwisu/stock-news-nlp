#  bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
# pip install mecab-python3
# pip install mecab-ko-dic
import pandas as pd
from konlpy.tag import Mecab
from tqdm import tqdm

df = pd.read_csv("../news_crawling.csv", index_col=0)

outfile = 'news_crawling-mecab.txt'
f = open(outfile, 'w')

mecab = Mecab()
for row in tqdm(df.itertuples(), total=df.shape[0]):
    title = getattr(row, 'title')
    noun_list = mecab.nouns(title.strip())
    for r in noun_list:
        f.write(r + '\n')

f.close()
