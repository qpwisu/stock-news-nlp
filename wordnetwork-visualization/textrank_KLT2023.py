# https://excelsior-cjh.tistory.com/93
from newspaper import Article # crawling package
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

from konlp.kma.klt2023 import klt2023
import nltk

def get_nouns(sentences):
    klt = klt2023()
    nouns = [' '.join(klt.nouns(str(sentence))) for sentence in sentences if sentence != '']
    return nouns

def text2sentences(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    return sentences

def url2text(url):
    article = Article(url, language = 'ko')
    article.download()
    article.parse()
    return article.text # a news data

def sentence_graph(nouns):
    tfidf = TfidfVectorizer()
    cnt_vec = CountVectorizer()
    tfidf_mat = tfidf.fit_transform(nouns).toarray()
    graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
    return graph_sentence

def word_graph(nouns):
    cnt_vec = CountVectorizer()
    cnt_vec_mat = normalize(cnt_vec.fit_transform(nouns).toarray().astype(float), axis = 0)
    vocab = cnt_vec.vocabulary_
    graph_word = np.dot(cnt_vec_mat.T, cnt_vec_mat)
    idx2word = {vocab[word] : word for word in vocab}
    return graph_word, idx2word

def get_ranks(graph, d = 0.85):
    G = graph
    matrix_size = G.shape[0]
    for idx in range(matrix_size):
        G[idx, idx] = 0 # diagonal
        link_sum = np.sum(G[:, idx])
        if link_sum != 0:
            G[:, idx] /= link_sum
        G[:, idx] *= -d
        G[idx, idx] = 1

    TR = (1-d)*np.ones((matrix_size, 1))
    ranks = np.linalg.solve(G, TR)
    return {idx:r[0] for idx, r in enumerate(ranks)}

def summarize(sort_rank_sent, sentences, sent_num=3):
    summary = []
    index = []

    for idx in sort_rank_sent[:sent_num]:
        index.append(idx)
    for idx in index:
        summary.append(sentences[idx])
    return summary

def keywords(sort_rank_word, idx2word, word_num = 10):
    keywords = []
    index = []

    for idx in sort_rank_word[:word_num]:
        index.append(idx)
    for idx in index:
        keywords.append(idx2word[idx])
    return keywords

def get_text():
    print("Ex) News URL -- https://newsis.com/view/?id=NISX20210607_0001467657&cID=10201&pID=10200")
    text = str(input('Input news URL, text file(test.txt), or quit: '))
    if text[:4] == 'http':
      text = url2text(text)	 # 네이버/다음 등의 뉴스기사 URL
    elif text[-4:] == '.txt':
      with open(text, 'r') as file:
        text = file.read()
    return text

if __name__== '__main__':
    while True:
        text = get_text()	# news URL, text file name, or 'quit'
        if text == 'quit':
          break

        sentences = text2sentences(text)
        nouns = get_nouns(sentences)

        graph_sentence = sentence_graph(nouns) # sentence to sentence graph
        graph_word, idx2word = word_graph(nouns) # word to word graph

        rank_sentence = get_ranks(graph_sentence) 
        sort_rank_sent = sorted(rank_sentence, key = lambda x:rank_sentence[x], reverse = True) # top rank sort
        rank_word = get_ranks(graph_word) 

        sort_rank_word = sorted(rank_word, key = lambda x:rank_word[x], reverse = True) # top rank sort

        #print('\nText =', sentences)
        i=1
        for sent in sentences:
            print(str(i)+'.', sent)
            i = i+1
        print('\nTop 20 keywords =', keywords(sort_rank_word, idx2word, word_num=20))

        summary_sentences = summarize(sort_rank_sent, sentences, sent_num=3)
        print('\nSummary sentences are:\n')
        i=1
        for sent in summary_sentences:
            print(str(i)+'.', sent, '\n')
            i = i+1
