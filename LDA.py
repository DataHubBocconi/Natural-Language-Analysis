# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:50:13 2017

@author: guglielmo
"""
import scipy.sparse as sps
import numpy as np
import os, re
import binary_search
import lda

def clean_book(text):
    text = re.sub(r'- \n','', text)
    text = re.sub(r'\n',' ',text)
    text = re.sub(r'\'s','',text)
    text = re.sub(r'[^a-zA-z ]', '',  text).lower()
    text = re.sub(r' {2,}',' ',text)
    text = re.sub(r' [a-zA-z] ', ' ', text)
    text = re.sub(r"( the | is | be | not | in | this | to | his | her | he | she | de | dat | a | about | above | after | again | against | all | am | an | and | any | are | aren't | as | at | be | because | been | before | being | below | between | both | but | by | can't | cannot | could | couldn't | did | didn't | do | does | doesn't | doing | don't | down | during | each | few | for | from | further | had | hadn't | has | hasn't | have | haven't | having | he | he'd | he'll | he's | her | here | here's | hers | herself | him | himself | his | how | how's | i | i'd | i'll | i'm | i've | if | in | into | is | isn't | it | it's | its | itself | let's | me | more | most | mustn't | my | myself | no | nor | not | of | off | on | once | only | or | other | ought | our | ours | ourselves | out | over | own | same | shan't | she | she'd | she'll | she's | should | shouldn't | so | some | such | than | that | that's | the | their | theirs | them | themselves | then | there | there's | these | they | they'd | they'll | they're | they've | this | those | through | to | too | under | until | up | very | was | wasn't | we | we'd | we'll | we're | we've | were | weren't | what | what's | when | when's | where | where's | which | while | who | who's | whom | why | why's | with | won't | would | wouldn't | you | you'd | you'll | you're | you've | your | yours | yourself | yourselves )",' ',text)
    words = text.split(' ')
    return words

def create_sparse_matrix(folder, word_list):
    '''
    create sparse matrix of size rows = number of words and columns = number of documents
    it goes through all the files and for each one updates the weight for the relative words contained
    the row index is the position of the word in the word_list (use binary_search)
    word_list is ordered
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
        with open(container[i],encoding = 'utf-8') as reader:
            doc = reader.read()
        words = clean_book(doc)
        for word in words:
            count += 1
            index = bin_search.binary_search_index(word_list, word)
            mtx[i, index] += 1
    os.chdir(folder)
    print('words:',count)
    return mtx

def make_word_list(folder):
    os.chdir(folder+"\\source")
    container = os.listdir()
    words_tot = []
    count = 0
    for i in range(len(container)):
        print(container[i])
        with open(container[i],encoding = 'utf-8') as reader:
            doc = reader.read()
        words = clean_book(doc)
        for word in words:
            words_tot.append(word)
            count += 1
    os.chdir(folder)
    print('words:',count)
    print('unique words:',len(set(words_tot)))
    return sorted(words_tot)

def get_vocab(mtx,doc,word_list):
    vocab = []
    for i in range(mtx.shape[1]):
        if mtx[doc,i]:
            vocab.append(word_list[i])
    return vocab
        

def main():
    word_list = make_word_list(os.getcwd())
    print('ready to create')
    mtx= create_sparse_matrix(os.getcwd(),word_list)
    print(mtx.shape)
    print('created')
    vocab=get_vocab(mtx,0,word_list)
    model = lda.LDA(n_topics = 5,n_iter=1000, refresh=10)
    print('preparing to fit')
    model.fit(mtx)
    print('fitting')
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(word_list)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        print(np.argsort(topic_dist)[:-(n_top_words+1):-1])
        
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
    
    
    
    
    
    
    
    
    
    
    