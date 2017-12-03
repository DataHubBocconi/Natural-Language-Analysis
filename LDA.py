# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:50:13 2017

"""
import scipy.sparse as sps
import numpy as np
import os
import binary_search
import lda
import BookAnalyzer
import time

def create_sparse_matrix(folder, word_list):
    '''
    create sparse matrix of size rows = number of documents and columns = number of words
    
    It goes through all the files and for each one updates the weight for the relative words.
    The row index is the position of the word in the word_list (use binary_search)
    
    word_list is the unique, ordered collection of all the words in the texts
    '''
    os.chdir(folder+"\\source")
    container = os.listdir()
    columns = len(word_list)
    rows = len(container)
    bin_search = binary_search.binary_search()
    mtx = sps.lil_matrix((rows, columns),dtype = np.int32)
    count = 0
    for i in range(len(container)):
        print(container[i])
        reader = open(container[i],encoding = 'utf-8')
        for line in reader:
            word = line.strip()
            count += 1
            index = bin_search.binary_search_index(word_list, word)
            mtx[i, index] += 1
        reader.close()
    os.chdir(folder)
    print('words:',count)
    return mtx

def make_word_list(folder):
    os.chdir(folder+"\\source")
    container = os.listdir()
    words_tot = []
    for i in range(len(container)):
        print(container[i])
        with open(container[i],encoding = 'utf-8') as reader:
            doc = reader.read()
        words = BookAnalyzer.clean_book(doc)
        words_tot.extend(words)
    os.chdir(folder)
    unique = set(words_tot)
    print('words:',len(words_tot))
    print('unique words:',len(unique))
    return sorted(unique)


def main():
    times = []
    times.append(time.time())
    word_list = make_word_list(os.getcwd())
    print('ready to create')
    mtx= create_sparse_matrix(os.getcwd(),word_list)
    print(mtx.shape)
    print('created')
    times.append(time.time())
    model = lda.LDA(n_topics = 5,n_iter=1000, refresh=1000)
    print('preparing to fit')
    model.fit(mtx)
    times.append(time.time())
    
    print("set-up time:",time[1]-time[0])
    print("lda time:",time[2]-time[1])
    
    print('fitting')
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(word_list)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        print(topic_dist[np.argsort(topic_dist)][:-(n_top_words+1):-1])
        
def test():
    X = lda.datasets.load_reuters()
    vocab = lda.datasets.load_reuters_vocab()
    return vocab
    titles = lda.datasets.load_reuters_titles()
    model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        print(i)
        print(topic_dist,'\n',np.argsort(topic_dist),len(topic_dist))
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
    
    
    
    
    
    
    
    
    
    