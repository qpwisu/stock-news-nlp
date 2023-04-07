from gensim.models import FastText
model = FastText.load("dataFile/fasttext.model")
# print(model.wv["삼성전자"])
print(model.wv.most_similar('카카오'))