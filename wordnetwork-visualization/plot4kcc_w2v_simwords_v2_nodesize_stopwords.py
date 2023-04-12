# -*- coding: utf-8 -*-
# python plot4kcc_w2v_simwords_v2_nodesize_stopwords.py 삼성전자 no cyan 5 5
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

		G.add_edge('사랑', '우정', weight=0.8807)
		G.add_edge('사랑', '기쁨', weight=0.7660)
		G.add_edge('우정','기쁨', weight=0.7826)
		G.add_edge('사랑', '슬픔', weight=0.6412)
		G.add_edge('우정','슬픔', weight=0.5603)
		G.add_edge('가정', '아버지', weight=0.2827)
		G.add_edge('가정', '어머니', weight=0.6951)
		G.add_edge('가족','사랑', weight=0.5363)
		G.add_edge('가족','기쁨', weight=0.5198)
		G.add_edge('어머니','사랑', weight=0.6545)
		G.add_edge('아버지','사랑', weight=0.3555)
		G.add_edge('어머니','사랑', weight=0.6098)

		G.add_edge('인생','굴레', weight=0.3555)
		G.add_edge('인생','행복', weight=0.6098)
		G.add_edge('인생','고통', weight=0.4098)

		return G

def visualization(G,imageFileName,nodecolor='skyblue',edgelabel='yes'):
		plt.figure(figsize=(15, 15), dpi=80)

		font_name = fm.FontProperties(fname="/System/Library/Fonts/AppleSDGothicNeo.ttc").get_name()
		rc('font', family=font_name)
		mpl.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
		
		elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
		esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
		
		pos=nx.spring_layout(G) # positions for all nodes
		
		# nodes
		d = dict(G.degree)
		#nx.draw(G,nodelist=d.keys(),node_size=[v*300 for v in d.values()])
		#nx.draw_networkx_nodes(G,pos,node_size=1500,node_color=nodecolor)	#default color: '#1f78b4'
		nx.draw_networkx_nodes(G,pos,node_size=[v*100+1000 for v in d.values()],
				node_color=nodecolor)	#default color: '#1f78b4'
		
		# edges
		nx.draw_networkx_edges(G,pos,edgelist=elarge,
				width=1.2,edge_color='blue')
		nx.draw_networkx_edges(G,pos,edgelist=esmall,
				width=1.2,alpha=0.5,edge_color='b',style='dashed')

		# edge labels
		if edgelabel=='yes':
				edge_weight = nx.get_edge_attributes(G,'weight')
				nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_weight)
		
		# labels
		nx.draw_networkx_labels(G,pos,font_family=font_name,font_size=14)

		plt.axis('off')
		plt.savefig('%s' %(imageFileName)) # save as png
		print('It was saved %s' %(imageFileName))
		plt.show() # display


from gensim.models import Word2Vec

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
		simWords = model.wv.most_similar(word,topn=n1)
		stopwords= ['오뚜', 'BGF리테', 'LF', 'GS리테']

		G=nx.Graph()
		for (w2,wgt) in simWords:	# 1차 확장
				if w2 not in stopwords:
				    G.add_edge(word,w2,weight=round(wgt,2))

		for (w2,wgt) in simWords:
				simWords2 = model.wv.most_similar(w2,topn=n2)
				for (w3,wgt) in simWords2:	# 2차 확장
						if w2 not in stopwords:
						    G.add_edge(w2,w3,weight=round(wgt,2))

		return G


if __name__ == "__main__":
		kword="사랑"
		color='skyblue'			# default: '#1f78b4'
		nsim1=5; nsim2=10		# number of similar words at level 1, 2
		elabel='yes'
		
		if len(sys.argv)==2:
				kword=sys.argv[1]
		elif len(sys.argv)==3:
				kword=sys.argv[1]; elabel=sys.argv[2] # yes / no
		elif len(sys.argv)==4:
				kword=sys.argv[1]; elabel=sys.argv[2]; color=sys.argv[3];
		elif len(sys.argv)==5:
				kword=sys.argv[1]; elabel=sys.argv[2]; # yes / no
				color=sys.argv[3]; nsim1=int(sys.argv[4]);
		elif len(sys.argv)==6:
				kword=sys.argv[1]; elabel=sys.argv[2]; # yes / no
				color=sys.argv[3]; nsim1=int(sys.argv[4]); nsim2=int(sys.argv[5])
		else:
				print("C> test.py keyword yes/no color nsim1 nsim2 True")
				print("C> test.py 우정")
				print("C> test.py 우정 no")
				print("C> test.py 연애 yes pink")
				print("C> test.py 사랑 no fuchsia 5 15")
				print("C> test.py 행복 yes skyblue 4 10")

#		model_name = "D:/KCC_word2vec/model/FastText-KCC150.model"
		# model_name = "word2vec-KCC150.model"
		model_name = "../news_word_embedding/dataFile/word2vec-KCC_news_mecab.model"
		# model_name = "word2vec-news_mecab.model"
		print('Loading word2vec model -- %s' %(model_name))
		model = Word2Vec.load(model_name)

		G = setEdges_test()
		fileName = "word-network-test.png"	# filename to save a image
		#visualization(G,fileName)

		#G = setEdges_test_w2v(model)
		G = setEdges_simWords(model,word=kword,n1=nsim1,n2=nsim2)
		fileName = "word-network.png"	# filename to save a image
		visualization(G,fileName,nodecolor=color,edgelabel=elabel)
