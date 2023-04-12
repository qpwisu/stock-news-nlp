# python generate_sentence_vectors.py 'dataFile/word2vec-KCC_news_mecab.model' 'dataFile/KCC_news_mecab.txt'
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import sys
import numpy as np
import pickle
from numpy import dot
from numpy.linalg import norm
from collections import defaultdict
from tqdm import tqdm



def generate_word2vec(model, sentence):
    tokens = sentence.split()

    sentence_vector = []
    for token in tokens:
        if model.wv.__contains__(token):
            vector = model.wv.get_vector(token)
            sentence_vector.append(vector)
    sentence_vector = np.array(sentence_vector)
    return np.average(sentence_vector, axis=0)

    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print("C> wv_test.py word2vec.model")
        exit()
    print("\nLoading Korean word embedding vectors for 'KMA tokenized text file'.\n")
    model_name = sys.argv[1]	# Word2Vec model -- 'word2vec-kowiki.model'
    model = Word2Vec.load(model_name)
    text_file = sys.argv[2]
    sentence_vectors = []

    with open(text_file, 'r', encoding='utf8') as f:
        for line in f:
            sentence_vector = generate_word2vec(model, line)
            sentence_vectors.append(sentence_vector)
    print('Successfully generated sentence vectors!')
    
    with open('dataFile/sentence_vectors.pkl', 'wb') as f:
        pickle.dump(sentence_vectors, f)

    print('Successfully saved sentence vectors!')
            

