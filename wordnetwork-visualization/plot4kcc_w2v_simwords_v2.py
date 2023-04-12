# -*- coding: utf-8 -*-
"""
An example using Graph as a weighted network.
"""
__author__ = """Kang Seung-Shik at Kookmin University, http://cafe.naver.com/nlpk"""

import sys

try:
    import matplotlib.pyplot as plt
except:
    raise

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from matplotlib import rc
import matplotlib as mpl
import networkx as nx

def setEdges_test():
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

def visualization(G,imageFileName,nodecolor='skyblue'):
		plt.figure(figsize=(15, 15), dpi=80)

		font_name = fm.FontProperties(fname="/System/Library/Fonts/AppleSDGothicNeo.ttc").get_name()
		rc('font', family=font_name)
		mpl.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
		
		elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
		esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
		
		pos=nx.spring_layout(G) # positions for all nodes
		
		# nodes
		nx.draw_networkx_nodes(G,pos,node_size=1500,node_color=nodecolor)	#default color: '#1f78b4'
		
		# edges
		nx.draw_networkx_edges(G,pos,edgelist=elarge,
				width=1.2,edge_color='blue')
		nx.draw_networkx_edges(G,pos,edgelist=esmall,
				width=1.2,alpha=0.5,edge_color='b',style='dashed')
		
		# labels
		nx.draw_networkx_labels(G,pos,font_family=font_name,font_size=14)

		plt.axis('off')
		plt.savefig('%s' %(imageFileName)) # save as png
		print('It was saved %s' %(imageFileName))
		plt.show() # display


from gensim.models import Word2Vec

def test1(model):
		# 유사 단어 topn개 출력 예제
		print('보수:', model.wv.most_similar('보수', topn=20))
		print('진보:', model.wv.most_similar('진보', topn=20))
		
		print('혐오:', model.wv.most_similar('혐오', topn=20))
		# print('성소수자:', model.wv.most_similar('성소수자', topn=20))
		print('혁신:', model.wv.most_similar('혁신', topn=5))
		
		print("(여배우-여자)+남자 =", model.wv.most_similar(positive=['여배우', '남자'], negative=['여자'], topn=10))
		print("(여왕-여자)+남자 =", model.wv.most_similar(positive=['여왕', '남자'], negative=['여자'], topn=10))
		print("(서울-대한민국)+일본 =", model.wv.most_similar(positive=['서울', '일본'], negative=['대한민국'], topn=10))
		print("희망+사랑-슬픔 =", model.wv.most_similar(positive=['희망', '사랑'], negative=['슬픔'], topn=3))
		print("sim(사랑,우정) =", model.wv.similarity('사랑', '우정'))


def test2(model):
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


def setEdges_test_w2v(model):
		w1_list=['사랑','우정','가족','아버지','어머니', '인생', '죽음', '이별']
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


def setEdges_simWords(model,word,n1=10,n2=5):
		simWords = model.wv.most_similar(word, topn=n1)

		G=nx.Graph()
		for (w2,wgt) in simWords:
		    G.add_edge(word,w2,weight=wgt)

		for (w2,wgt) in simWords:
				simWords2 = model.wv.most_similar(w2, topn=n2)
				for (w3,wgt) in simWords2:
				    G.add_edge(w2,w3,weight=wgt)

		return G


if __name__ == "__main__":
		kword="사랑"
		color='skyblue'			# default: '#1f78b4'
		nsim1=5; nsim2=15		# number of similar words at level 1, 2
		
		if len(sys.argv)==2:
				kword=sys.argv[1]
		elif len(sys.argv)==3:
				kword=sys.argv[1]; color=sys.argv[2];
		elif len(sys.argv)==4:
				kword=sys.argv[1]; color=sys.argv[2]; nsim1=int(sys.argv[3])
		elif len(sys.argv)==5:
				kword=sys.argv[1]; color=sys.argv[2];
				nsim1=int(sys.argv[3]); nsim2=int(sys.argv[4])
		else:
				print("C> test.py keyword color nsim1 nsim2")
				print("C> test.py 우정")
				print("C> test.py 연애 pink")
				print("C> test.py 사랑 fuchsia 5 15")
				print("C> test.py 행복 skyblue 4 10")

#		model_name = "D:/KCC_word2vec/model/FastText-KCC150.model"
		# model_name = "word2vec-KCC150.model"
		model_name = "../news_word_embedding/dataFile/word2vec-KCC_news_mecab.model"

		# model_name = "word2vec-news_mecab.model"
		print('Loading word2vec model -- %s' %(model_name))
		model = Word2Vec.load(model_name)

		
		test1(model)
		#test2(model)

		G = setEdges_test()
		fileName = "word-network-test.png"	# filename to save a image
		#visualization(G,fileName)

		#G = setEdges_test_w2v(model)
		G = setEdges_simWords(model,word=kword,n1=nsim1,n2=nsim2)
		fileName = "word-network.png"	# filename to save a image
		visualization(G,fileName,nodecolor=color)
