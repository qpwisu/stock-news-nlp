# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
An example using Graph as a weighted network.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""

try:
    import matplotlib.pyplot as plt
except:
    raise

#import pandas as pd
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

def visualization(G):
		font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
		rc('font', family=font_name)
		mpl.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
		
		elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
		esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
		
		pos=nx.spring_layout(G) # positions for all nodes
		
		# nodes
		nx.draw_networkx_nodes(G,pos,node_size=600)
		
		# edges
		nx.draw_networkx_edges(G,pos,edgelist=elarge,width=1.2,edge_color='r')
		nx.draw_networkx_edges(G,pos,edgelist=esmall,width=1.2,alpha=0.5,edge_color='b',style='dashed')
	
		# labels
		nx.draw_networkx_labels(G,pos,font_family=font_name,font_size=12)
		
		plt.axis('off')
		plt.savefig("word-network.png") # save as png
		print('It was saved %s' %("word-network.png"))
		plt.show() # display

if __name__ == "__main__":
		G = test_setEdges()
		visualization(G)