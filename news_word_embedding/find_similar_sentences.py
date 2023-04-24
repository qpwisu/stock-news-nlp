# python find_similar_sentences.py dataFile/word2vec-KCC_news_mecab.model dataFile/sentence_vectors.pkl
from gensim.models import Word2Vec
import sys
import numpy as np
import pickle
from numpy import dot
from numpy.linalg import norm
from collections import defaultdict
from tqdm import tqdm
import pandas as pd
def calculate_cosine_similarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))

def find_similar_sentences(model, idx, sentence_vectors, raw_sentences, n):
    target_sentence_vector = sentence_vectors[idx]
    similarity_list = []
    similar_sentences = []

    # target문장과 나머지 문장간의 유사도 측정하여 유사도 상위 5개 문장 추출 
    for i in range(len(sentence_vectors)):
        if i == idx or raw_sentences[i] == raw_sentences[idx]:
            continue
        similarity = calculate_cosine_similarity(target_sentence_vector, sentence_vectors[i])
        if  type(similarity) != np.float32:
            continue
        similarity_list.append((i, similarity))
    
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    if not similarity_list:
        return similar_sentences
    print(similarity_list[:n])
    # 유사도 높은 순서대로 raw sentence와 맵핑
    for i in range(n):

        _idx, similarity = similarity_list[i]
        raw_sentence = raw_sentences[_idx]
        similar_sentences.append([raw_sentence, similarity])

    return similar_sentences


if __name__=="__main__":
    if len(sys.argv) < 2:
        print("C> wv_test.py word2vec.model")
        exit()
    print("\nLoading Korean word embedding vectors for 'KMA tokenized text file'.\n")
    model_name = sys.argv[1]    # Word2Vec model -- 'word2vec-kowiki.model'
    model = Word2Vec.load(model_name)
    vector_file = sys.argv[2]
    raw_sentences = []
    target_idx = 2
    n = 5

    filename = "dataFile/KCC150_Korean_sentences_utf_8.txt"
    f = open(filename, "r", encoding='utf-8')
    text = f.readlines()
    f.close()
    for sent in text:
        # if sent == "":
        #     continue
        raw_sentences.append(sent.strip())

    sentences2 = []
    filename = "dataFile/KCC150_Korean_sentences_utf_8.txt"
    f = open(filename, "r", encoding='utf-8')
    text = f.readlines()
    f.close()
    for sent in text:
        sentences2.append(sent.strip())


    with open(vector_file, 'rb') as f:
        sentence_vectors = pickle.load(f)
    print('Successfully loaded sentence vectors!')

    for idx in range(4400,4405):
        print(idx)
        similarity_sentences = find_similar_sentences(model, idx, sentence_vectors, raw_sentences, n)
        if len(similarity_sentences) == 0:
            continue
        print("원본 문장: ", raw_sentences[idx])
        for i in range(n):
            print("--> ", similarity_sentences[i])