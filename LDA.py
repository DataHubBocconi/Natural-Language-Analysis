# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:50:13 2017

"""
import scipy.sparse as sps
import numpy as np
import os
import binary_search
import lda
import cleanBook
import time

def compute_result(n_iter = 2000, n_topic = 5, n_top_words = 15):
    start_time = time.time()
    _init()
    word_list = _make_word_list()
    mtx= _create_sparse_matrix(word_list)
    model = lda.LDA(n_topics = n_topic,n_iter=n_iter, refresh=n_iter)
    model.fit(mtx)
    end_time = time.time()
    
    topic_word = model.topic_word_
    n_top_words = n_top_words
    vocabulary = []
    frequencies = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(word_list)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        vocabulary.append(topic_words)
        frequencies.append(topic_dist[np.argsort(topic_dist)][:-(n_top_words+1):-1])
    tot_words = mtx.sum()
    #n_topic, n_iter, n_doc, n_unique_words, n_total_words, n_top_words, elapsed_time
    statistics = (n_topic, n_iter, mtx.shape[0], mtx.shape[1], tot_words, n_top_words, end_time - start_time)
    _handle_output(vocabulary, frequencies, statistics, n_topic)
        
def compute_result_topics(n_iter = 2000, n_topics = 5, n_top_words = 30):
    '''Carries out the analysis for multiple topics, specifically for
    range(1, n_topics+1). So it will do n_topics analyses and produce 
    n_topics reports. It does so more efficiently then multiple calls
    to compute_result() with different values for n_topic.
    This function assumes that the documents in source are not changed
    throughout the course of operation.
    Note how n_topics parameter here changes meaning w.r.t. compute_result()
    '''
    _init()
    word_list = _make_word_list()
    mtx= _create_sparse_matrix(word_list)
    tot_words = mtx.sum()
    for n_topic in range(1, n_topics+1):
        start_time = time.time()
        model = lda.LDA(n_topics=n_topic, n_iter=n_iter, refresh=n_iter)
        model.fit(mtx)
        end_time = time.time()
        topic_word = model.topic_word_
        vocabulary = []
        frequencies = []
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(word_list)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            vocabulary.append(topic_words)
            frequencies.append(topic_dist[np.argsort(topic_dist)][:-(n_top_words+1):-1])
        #n_topic, n_iter, n_doc, n_unique_words, n_total_words, n_top_words, elapsed_time
        statistics = (n_topic, n_iter, mtx.shape[0], mtx.shape[1], tot_words, n_top_words, end_time - start_time)
        _handle_output(vocabulary, frequencies, statistics, n_topic)

def _handle_output(vocabulary, frequencies, statistics, n_topic, path=os.getcwd()):
    freq = []
    for topic in frequencies:
        freq.append([str(elem) for elem in topic])
    text = []
    text.append("n_topic,%s,n_iter,%s,n_documents,%s,n_unique_words,%s,n_total_words,%s,n_top_words,%s,elapsed_time(seconds),%s\n"%(statistics))
    for words, frequence in zip(vocabulary, freq):
        text.append(",".join(words))
        text.append(",".join(frequence))
    with open(path+os.sep+'result'+os.sep+str(n_topic)+'.csv', 'w', encoding='utf-8') as writer:
        writer.write("\n".join(text))
    files = os.listdir(path+os.sep+'source')
    with open(path+os.sep+'result'+os.sep+"source.txt", 'w', encoding='utf-8') as writer:
        writer.write("\n".join(files))
    
        

def _create_sparse_matrix(word_list, path = os.getcwd()):
    '''
    create sparse matrix of size rows = number of documents and columns = number of words
    
    It goes through all the files and for each one updates the weight for the relative words.
    The row index is the position of the word in the word_list (use binary_search)
    
    word_list is the unique, ordered collection of all the words in the texts
    '''
    container = os.listdir(path+os.sep+'source')
    columns = len(word_list)
    rows = len(container)
    bin_search = binary_search.binary_search()
    mtx = sps.lil_matrix((rows, columns),dtype = np.int32)
    i = 0
    for file in container:
        if _check_temp_read(file, path):
            reader = open(path+os.sep+"temp"+os.sep+'_'+file, encoding='utf-8')
            for line in reader:
                word = line.rstrip('\n')
                index = bin_search.binary_search_index(word_list, word)
                mtx[i, index] += 1
            reader.close()
        else:
            with open(path+os.sep+"source"+os.sep+file, encoding='utf-8') as reader:
                text = reader.read()
            words = cleanBook.clean_book(text)
            for word in words:
                index = bin_search.binary_search_index(word_list, word)
                mtx[i, index] += 1
        i = i + 1
    return mtx

def _make_word_list(path=os.getcwd()):
    container = os.listdir(path+os.sep+"source")
    words_unique = set()
    for file in container:
        if _check_temp_read(file, path):
            reader = open(path+os.sep+"temp"+os.sep+'_'+file, encoding='utf-8')
            for line in reader:
                word = line.rstrip('\n')
                words_unique.add(word)
            reader.close()
        else:
            with open(path+os.sep+"source"+os.sep+file, encoding='utf-8') as reader:
                text = reader.read()
            words = cleanBook.clean_book(text)
            words_unique.update(words)
            _write_temp(words, path, file)
    return sorted(words_unique)
            
def _check_temp_read(file, path):
    if os.path.exists(path+os.sep+'temp'+os.sep+'_'+file):
        return True
    else:
        return False

def _write_temp(words, path, file):
    with open(path+os.sep+'temp'+os.sep+'_'+file, 'w', encoding='utf-8') as writer:
        writer.write("\n".join(words))

def _init(path = os.getcwd()):
    '''does initial check on directories and files to be analyzed
    '''
    source = path+os.sep+'source'
    temp = path+os.sep+'temp'
    result = path+os.sep+'result'
    if os.path.isdir(source):
        l = os.listdir(source)
        if len(l) != 0:
            for file in l:
                if os.path.splitext(source+os.sep+file)[1] != '.txt':
                    raise Exception('Found a file in source folder which is not a .txt file format')
        else:
            raise Exception('No files found in the source folder')
    else:
        raise Exception('No source folder found')
        
    if not os.path.isdir(temp):
        os.mkdir(temp)
    if not os.path.isdir(result):
        os.mkdir(result)
    #clear result
    for file in os.listdir(result):
        os.remove(result+os.sep+file)