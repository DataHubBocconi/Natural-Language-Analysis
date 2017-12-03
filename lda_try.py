#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:20:14 2017

@author: renatoberlinghieri
"""
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os
import glob
import re
import nltk
import time





def build_lil(): 
    path = os.getcwd()
    os.chdir(path+r"\source")
    files = glob.glob('*.txt')
    books = []
    for title in files:
        with open(title,encoding='utf-8') as reader:
            text_stemmed = reader.read()
        text_stemmed = text_stemmed.split("\n")
        text_stemmed.pop()
        books.append(text_stemmed)
    return books
    #The output of this function is a list of lists, one list for each of our original documents, tokenized, stopped and stemmed.
    
   

def lda_running(n_passes = 20, n_words = 8):  
    n_topics = 5
    times = []
    times.append(time.time())
    books = build_lil()
    
    # turn our tokenized documents into a id <-> term dictionary
    #The Dictionary() function traverses texts, assigning a unique integer id to each unique token while 
    #also collecting word counts and relevant statistics. To see each token’s unique integer id, try print(dictionary.token2id).

    dictionary = corpora.Dictionary(books)
        
    # convert tokenized documents into a document-term matrix
    #The doc2bow() function converts dictionary into a bag-of-words. The result, corpus, is a list of vectors 
    #equal to the number of documents. In each document vector is a series of tuples in which we can see if a word is there and how many times it shows up 
    corpus = [dictionary.doc2bow(text) for text in books]
    
    # generate LDA model
    #Parameters:
    #num_topics: required. An LDA model requires the user to determine how many topics should be generated. Our document set is small, so we’re only asking for three topics.
    #id2word: required. The LdaModel class requires our previous dictionary to map ids to strings.
    #passes: optional. The number of laps the model will take through corpus. The greater the number of passes, the more accurate the model will be. A lot of passes can be slow on a very large corpus.
    times.append(time.time())
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = n_topics, id2word = dictionary, passes = n_passes)
    
    lda_result = ldamodel.print_topics(num_topics = n_topics, num_words = n_words)
    times.append(time.time())
    print("set-up time:",times[1]-times[0])
    print("lda time:",times[2]-times[1])
    for i in lda_result:
        print(i)
    return lda_result
    





