from gensim.models import FastText
import sys


def wv_KMA_tokens_train():

    filename = "dataFile/KCC_news_mecab.txt"
    f = open(filename, "r", encoding='utf-8')
    text = f.readlines()
    f.close()
    tokens = []
    for sent in text:
        tokens.append(sent.split())
    # vector_size = 벡터 차원, window = 훈랸시 앞 뒤로 고려하는 단어 수, min_count : 해당 빈도수보다 작게 등장하면 배제, worker : 스레드 갯수 지정
    model = FastText(sentences=tokens, vector_size=300, window=5, min_count=2, workers=4)

    model_file = 'dataFile/fasttext.model'
    model.save(model_file)
    return model


if __name__ == "__main__":
    model = wv_KMA_tokens_train()  # 'KMA tokenized text file'

