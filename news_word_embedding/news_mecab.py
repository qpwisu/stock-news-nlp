#  bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
# iconv -c -f euc-kr -t utf-8 KCC150_Korean_sentences_EUCKR.txt > KCC150_Korean_sentences_utf_8.txt
# pip install mecab-python3
# pip install mecab-ko-dic
import pandas as pd
from konlpy.tag import Mecab
from tqdm import tqdm

# kcc와 크롤링한 데이터 합치기 37만개
# kcc = "dataFile/KCC150_Korean_sentences_utf_8.txt"
# k = open(kcc,'w')
# df = pd.read_csv("dataFile/news.csv", index_col=0)
# for row in tqdm(df.itertuples(), total=df.shape[0]):
#     title = getattr(row, 'title')
#     k.write(title + '\n')

openfile = "dataFile/KCC150_Korean_sentences_utf_8.txt"
outfile = "dataFile/KCC_news_mecab.txt"
f = open(openfile, 'r')
f2 = open(outfile,'w')
mecab = Mecab()
text = f.readlines()
f.close()

for sent in tqdm(text):
    noun_list = mecab.nouns(sent.strip())
    f2.write(" ".join(noun_list) + '\n')
f2.close()

