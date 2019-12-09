import pandas as pd

import unicodedata
import re
import json
import os

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import acquire

def normalize(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def replace_with_quote(string):
    return re.sub(r'a-z0-9\s', "'", string)

def basic_clean(string):
    string = string.lower()
    string = normalize(string)
    string = replace_with_quote(string)
    string = string.strip()
    return string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

def stem(text):
    stemmer = nltk.porter.PorterStemmer()
    words = text.split()
    stems = [stemmer.stem(word) for word in words]
    stem_string = ' '.join(stems)
    return stem_string

def lemmatize(text):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in text.split()]
    lemma_string = ' '.join(lemmas)
    return lemma_string

def remove_stopwords(text, extra_words=[], exclude_words=[]):
    text = tokenize(text)

    text = text.split()
    stopword_list = stopwords.words('english')

    stopword_list = set(stopword_list).difference(set(exclude_words))
    stopword_list = stopword_list.union(set(extra_words))

    filtered = []
    for word in text:
        if word not in stopword_list:
            filtered.append(word)
    text = " ".join(filtered)
    return text

def prepare_article_data(df):
    df['original'] = df.content
    df['cleaned'] = df.original.apply(basic_clean).apply(remove_stopwords)
    df['stemmed'] = df.cleaned.apply(stem)
    df['lemmatized'] = df.cleaned.apply(lemmatize)
    df.drop(columns='content', inplace=True)
    return df

def get_prepped(csv, fresh=False):
    if os.path.exists('prepped' + csv) and not fresh:
        df = pd.read_csv('prepped' + csv)
    else:
        df = pd.read_csv(csv)
        df = prepare_article_data(df)
        df.to_csv('prepped' + csv)
    return df