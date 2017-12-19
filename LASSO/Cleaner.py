#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:48:53 2017

@author: DataHubBocconi
"""
import stop_words,re, nltk, glob, os
import pandas as pd
def clean_book(book_path):
    '''
    :param book_path: complete path of document
    :return: stemmed and cleaned document
    '''
    with open(book_path, encoding='latin-1') as reader:
        book = reader.read()
    stemmed = clean_book(book)
    return stemmed


def clean_book(text, min_length=4):
    '''Removes stopwords and unuseful characters from a string.

    Takes in input the text as string and an optional parameter
    min_length, the length of all the words in outpt will be at
    least min_length. The default is 4.

    Outputs a list of words.
    '''
    # N.B. the order of the following operations is important!
    # remove header
    # text = re.sub(r'.{0,133}', '', text, 1, re.S)
    # remove links (must be done before symbol rem.)
    text = re.sub(r'http\S+', '', text)
    # remove genitivo sassone (must be done before symbol rem.)
    text = re.sub(r'\'s', '', text)
    # handle new-line that separates whole words (like considered
    # might become con- \nsidered
    text = re.sub(r'- \n', '', text)
    # removes unnecessary apostrophes (all those not forming contraction)
    text = re.sub(r"'+(?=\s) | (?<=\s)'+", ' ', text)
    # remove symbols
    text = re.sub(r"[^a-zA-Z0-9_\s'-]", '', text)
    # remove stand-alone words (made of any character
    # of length from one to min_length: {1,min_length}
    text = re.sub(r'(?<=\s).{1,' + str(min_length - 1) + r'}(?=\s)', '', text)
    # remove numbers
    text = re.sub(r'(?<=\s)[0-9_-]+(?=[\s.,])', '', text)
    # remove new lines
    text = re.sub(r'\n', ' ', text)
    text = text.lower()
    # Removes all the stopwords (words which are not characterizing for the meaning of the text)
    for word in stop_words.get_stop_words('english'):
        if len(word) >= min_length:
            text = re.sub(' ' + word + ' ', ' ', text)
    # Removes all the unnecessary spaces.
    text = re.sub(r' {2,}', ' ', text)
    words = text.split(' ')
    words.pop()
    # Stems the words
    stemmed = []
    errors = []
    for word in words:
        try:
            stemmed.append(nltk.PorterStemmer().stem(word))
        except IndexError:
            errors.append(word)
    if len(errors) != 0:
        print('Warning: errors found during stemming. Follows list of not-working words.')
        print(errors)
    return stemmed