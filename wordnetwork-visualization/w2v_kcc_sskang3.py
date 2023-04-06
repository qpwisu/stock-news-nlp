# -*- coding: utf-8 -*-
# EUC-KR encoding: "euc-kr"
#!/usr/bin/python

import os, sys

# http://nlp.kookmin.ac.kr/kcc/word2vec/
# http://nlp.kookmin.ac.kr/kcc/word2vec/demo


# Download FastText-KCC150.zip -- "FastText pre-training model for KCC150"
# One of the word2vec pre-training model in "http://nlp.kookmin.ac.kr/kcc/word2vec"
# Install Python and 'gensim' library, and then running
# C> pip install gensim"
# C> python

from gensim.models import Word2Vec

def test1():
		# 유사 단어 topn개 출력 예제
		print('보수:', model.wv.most_similar('보수', topn=20))
		print('진보:', model.wv.most_similar('진보', topn=20))
		
		print('혐오:', model.wv.most_similar('혐오', topn=20))
		print('성소수자:', model.wv.most_similar('성소수자', topn=20))
		print('혁신:', model.wv.most_similar('혁신', topn=5))
		
		print("(여배우-여자)+남자 =", model.wv.most_similar(positive=['여배우', '남자'], negative=['여자'], topn=10))
		print("(여왕-여자)+남자 =", model.wv.most_similar(positive=['여왕', '남자'], negative=['여자'], topn=10))
		print("(서울-대한민국)+일본 =", model.wv.most_similar(positive=['서울', '일본'], negative=['대한민국'], topn=10))
		print("희망+사랑-슬픔 =", model.wv.most_similar(positive=['희망', '사랑'], negative=['슬픔'], topn=3))
		print("sim(사랑,우정) =", model.wv.similarity('사랑', '우정'))


def test2():
		print('사랑:', model.wv.most_similar('사랑', topn=20))
		print('우정:', model.wv.most_similar('우정', topn=20))
		print('기쁨:', model.wv.most_similar('기쁨', topn=20))
		print('슬픔:', model.wv.most_similar('슬픔', topn=20))
		#print(model.wv['사랑'])
		#print(model.wv['우정'])
		#print(model.wv['기쁨'])
		#print(model.wv['슬픔'])

		print('기쁨+사랑-슬픔 =', model.wv.most_similar(positive=['기쁨', '사랑'], negative=['슬픔'], topn=1))
		print(model.wv.similarity('사랑', '우정'))
		print(model.wv.similarity('사랑', '기쁨'))
		print(model.wv.similarity('우정','기쁨'))
		print(model.wv.similarity('사랑', '슬픔'))
		print(model.wv.similarity('우정','슬픔'))
		print(model.wv.similarity('가족', '아버지'))
		print(model.wv.similarity('가족', '어머니'))
		print(model.wv.similarity('가족','사랑'))

		print(model.wv.similarity('가족','기쁨'))
		print(model.wv.similarity('어머니','사랑'))
		print(model.wv.similarity('아버지','사랑'))
		print(model.wv.similarity('어머니','기쁨'))
		print(model.wv.similarity('인생','불안'))
		print(model.wv.similarity('죽음','불안'))
		print(model.wv.similarity('인생','고통'))
		print(model.wv.similarity('죽음','고통'))
		print(model.wv.similarity('사랑','불안'))
		print(model.wv.similarity('이별','고통'))
		#print(model.wv.similarity('Freude','Schadenfreude'))
		#print(model.wv.similarity('Schadenfreude','Neid'))

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import matplotlib as mpl
import networkx as nx

def test_setEdges():
		G=nx.Graph()

		G.add_edge('사랑', '우정', weight=0.8807795)
		G.add_edge('사랑', '기쁨', weight=0.766035)
		G.add_edge('우정','기쁨', weight=0.7826214)
		G.add_edge('사랑', '슬픔', weight=0.641202)
		G.add_edge('우정','슬픔', weight=0.56035805)
		G.add_edge('가정', '아버지', weight=0.2827779)
		G.add_edge('가정', '어머니', weight=0.69517916)
		G.add_edge('가족','사랑', weight=0.53635)
		G.add_edge('가족','기쁨', weight=0.51986694)
		G.add_edge('어머니','사랑', weight=0.6545886)
		G.add_edge('아버지','사랑', weight=0.35554564)
		G.add_edge('어머니','사랑', weight=0.60982907)
		G.add_edge('인생','굴레', weight=0.35554564)
		G.add_edge('인생','행복', weight=0.60982907)
		G.add_edge('인생','고통', weight=0.40982907)
		return G


def setEdges():
		w1_list=['사랑','우정','가족','아버지','어머니', '인생', '죽움', '이별']
		w2_list=['사랑','우정','기쁨', '슬픔', '아버지', '어머니', '불안', '고통']
		w1_set = set(w1_list)
		w2_set = set(w2_list)

		available_set = []
		for w1, w2 in zip(w1_set, w2_set):
		    try:
		        score=model.wv.similarity(w1,w2)
		        available_set.append((w1,w2,score))
		    except Exception as e:
		        print(e)

		G=nx.Graph()
		for (w1,w2,wgt) in available_set:
		    G.add_edge(w1,w2,weight=wgt)

		return G


def visualization(G,imageFileName):
		font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
		rc('font', family=font_name)
		mpl.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결

		elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
		esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
		pos=nx.spring_layout(G) # positions for all nodes

		# nodes
		nx.draw_networkx_nodes(G,pos,node_size=600)

		# edges
		nx.draw_networkx_edges(G,pos,edgelist=elarge,width=4,edge_color='g')
		nx.draw_networkx_edges(G,pos,edgelist=esmall,width=4,alpha=0.5,edge_color='b',style='dashed')

		# labels
		nx.draw_networkx_labels(G,pos,font_size=16,font_family='sans-serif')

		plt.axis('off')
		plt.savefig('%s' %(imageFileName)) # save as png
		print('It was saved %s' %(imageFileName))
		plt.show() # display


if __name__ == "__main__":
#		model_name = "D:/KCC_word2vec/model/FastText-KCC150.model"
		model_name = "D:/KCC_word2vec/model/word2vec-KCC150.model"
		print('Loading word2vec model -- %s' %(model_name))
		model = Word2Vec.load(model_name)
		
		test1()
		#test2()

		G = test_setEdges()
		fileName = "word-network1.png"	# filename to save a image
		visualization(G, fileName)

		G = setEdges()
		fileName = "word-network2.png"	# filename to save a image
		visualization(G, fileName)

### Check the path!!!
# if sys.platform == "Windows":
#    model.save('i:/gensim/kcc/KMU3m.bin')
# else:
#    model.save('%s.bin' %infilename)
########################
