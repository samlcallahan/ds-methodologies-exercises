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
    return

def lemmatize(text):

    return

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

def prep_article(article_dict):
    for key in article_dict:
        something = 0
        prepped = []
    return prepped

def prepare_article_data(article_list):
    if type(article_list) is pd.DataFrame:
        article_list = article_list.to_dict('records')
    for article in article_list:
        article = prep_article(article)
    df = pd.DataFrame(article_list)
    df.to_csv('prepped_articles.csv')
    return df

def get_prepped(csv):
    if os.path.exists('prepped' + csv):
        df = pd.read_csv('prepped' + csv)
    else:
        df = pd.read_csv(csv)
        df = prepare_article_data(df)
    return df