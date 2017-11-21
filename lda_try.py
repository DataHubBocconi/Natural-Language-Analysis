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



def clean_book(book):
    print('Book opened')
    file = open(book,encoding='utf-8')
    # Open the book and import it as a string
    text = file.read()
    print('Book read')
    # Remove all the characters which are used by Python to go to a new line
    text = re.sub(r'- \n','', text)
    text = re.sub(r'\n',' ',text)
    print('New lines removed')
    # Here we start cleaning the text, we will tokenize it at the end to make the process 
    # more efficient
    # Remove the genitivo sassone
    text = re.sub(r'\'s','',text)
    # Remove everything which is not a letter, thus punctuation and numbers. 
    # Then it lower-cases everything
    text = re.sub(r'[^a-zA-z ]', '',  text).lower()
    # Removes all the unnecessary spaces.
    text = re.sub(r' {2,}',' ',text)
    text = re.sub(r' [a-zA-z] ', ' ', text)
    print('Non-letters removed')
    #f = re.sub(r'( a | about | above | after | again | against | all | am | an | and | any | are | aren\'t | as | at | be | because | been | before | being | below | between | both | but | by | can\'t | cannot | could | couldn\'t | did | didn\'t | do | does | doesn\'t | doing | don\'t | down | during | each | few | for | from | further | had | hadn\'t | has | hasn\'t | have | haven\'t | having | he | he\'d | he\'ll | he\'s | her | here | here\'s | hers | herself | him | himself | his | how | how\'s | i | i\'d | i\'ll | i\'m | i\'ve | if | in | into | is | isn\'t | it | it\'s | its | itself | let\'s | me | more | most | mustn\'t | my | myself | no | nor | not | of | off | on | once | only | or | other | ought | our | ours | ourselves | out | over | own | same | shan\'t | she | she\'d | she\'ll | she\'s | should | shouldn\'t | so | some | such | than | that | that\'s | the | their | theirs | them | themselves | then | there | there\'s | these | they | they\'d | they\'ll | they\'re | they\'ve | this | those | through | to | too | under | until | up | very | was | wasn\'t | we | we\'d | we\'ll | we\'re | we\'ve | were | weren\'t | what | what\'s | when | when\'s | where | where\'s | which | while | who | who\'s | whom | why | why\'s | with | won\'t | would | wouldn\'t | you | you\'d | you\'ll | you\'re | you\'ve | your | yours | yourself | yourselves )', ' ', e)
    # Removes all the stopwords (words which are not characterizing for the meaning of the text)
#   text = re.sub(r"( a | the | is | has | de | dat | not | to| in | her | his | he | she | we | us | you | it | about | above | after | again | against | all | am | an | and | any | are | aren't | as | at | be | because | been | before | being | below | between | both | but | by | can't | cannot | could | couldn't | did | didn't | do | does | doesn't | doing | don't | down | during | each | few | for | from | further | had | hadn't | has | hasn't | have | haven't | having | he | he'd | he'll | he's | her | here | here's | hers | herself | him | himself | his | how | how's | i | i'd | i'll | i'm | i've | if | in | into | is | isn't | it | it's | its | itself | let's | me | more | most | mustn't | my | myself | no | nor | not | of | off | on | once | only | or | other | ought | our | ours | ourselves | out | over | own | same | shan't | she | she'd | she'll | she's | should | shouldn't | so | some | such | than | that | that's | the | their | theirs | them | themselves | then | there | there's | these | they | they'd | they'll | they're | they've | this | those | through | to | too | under | until | up | very | was | wasn't | we | we'd | we'll | we're | we've | were | weren't | what | what's | when | when's | where | where's | which | while | who | who's | whom | why | why's | with | won't | would | wouldn't | you | you'd | you'll | you're | you've | your | yours | yourself | yourselves )",' ',text)
    stop_words = ["the","is","be","not","in","this","to","his","her","he","she","de","dat","a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
    for i in stop_words:
        text = re.sub(' ' + i + ' ',' ', text)
    print('Stop-words removed')
    # Tokenize the clean text
    words = text.split(' ')
    print('Tokenized')
    print('There are ',len(words), ' words')
    # Stems the words
    stemmed = [nltk.PorterStemmer().stem(t) for t in words]
    print('Stemmed')
    return stemmed




def build_lil(): 
    files = glob.glob('*.txt')
    books = []
    for title in files:
        text_stemmed = clean_book(title)
        books.append(text_stemmed)
    return books
    #The output of this function is a list of lists, one list for each of our original documents, tokenized, stopped and stemmed.
    
   

def lda_running(mydir = '/Users/renatoberlinghieri/Desktop/try_txt_sessodroga', n_topics = 8, n_passes = 20, n_words = 10):  
    
    os.chdir(mydir) 
    
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
    
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = n_topics, id2word = dictionary, passes = n_passes)
    
    lda_result = ldamodel.print_topics(num_topics = n_topics, num_words = n_words)
    
    return lda_result
    





