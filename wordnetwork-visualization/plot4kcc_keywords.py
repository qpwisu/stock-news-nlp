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

import textrank_KLT2000 as klt
def get_keywords():
    text = klt.get_text()	# news URL, text file name, or 'quit'
    if text == 'quit':
	      exit()

    sentences = klt.text2sentences(text)
    nouns = klt.get_nouns(sentences)

    graph_sentence = klt.sentence_graph(nouns) # sentence to sentence graph
    graph_word, idx2word = klt.word_graph(nouns) # word to word graph

    rank_sentence = klt.get_ranks(graph_sentence) 
    sort_rank_sent = sorted(rank_sentence, key = lambda x:rank_sentence[x], reverse = True) # top rank sort
    rank_word = klt.get_ranks(graph_word) 

    sort_rank_word = sorted(rank_word, key = lambda x:rank_word[x], reverse = True) # top rank sort
    
    return rank_word,sort_rank_word,idx2word

def setEdges_keywords(seed='keywords', n=20):
		stopwords= ['오뚜', 'BGF리테', 'LF', 'GS리테']
		rank_word,idx,idx2word=get_keywords()
		
		#centerword = seed
		centerword = idx2word[idx[0]]

		G=nx.Graph()
		n=min(n,len(rank_word))
		for i in range(1,n):
				if idx2word[idx[i]] not in stopwords:
				    G.add_edge(centerword,idx2word[idx[i]],weight=round(rank_word[idx[i]],2))

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


if __name__ == "__main__":
		kword="KEYWORDS"
		color='skyblue'			# default: '#1f78b4'
		nsim1=20; nsim2=10		# number of similar words at level 1, 2
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

		G=setEdges_keywords(kword,nsim1)
		fileName = "word-network-FILE.png"	# filename to save a image
		visualization(G,fileName,nodecolor=color,edgelabel=elabel)
		exit()
		
#		model_name = "D:/KCC_word2vec/model/FastText-KCC150.model"
		model_name = "D:/KCC_word2vec/model/word2vec-KCC150.model"
		print('Loading word2vec model -- %s' %(model_name))
		model = Word2Vec.load(model_name)

		G = setEdges_test()
		fileName = "word-network-test.png"	# filename to save a image
		#visualization(G,fileName)

		#G = setEdges_test_w2v(model)
		G = setEdges_simWords(model,word=kword,n1=nsim1,n2=nsim2)
		fileName = "word-network.png"	# filename to save a image
		visualization(G,fileName,nodecolor=color,edgelabel=elabel)
