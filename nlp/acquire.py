from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

BLOG_URLS = [
        "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
        "https://codeup.com/data-science-myths/",
        "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
        "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
        "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/",
    ]

def get_article(url):
    headers = {'user-agent': 'Codeup Bayes Sam'}
    response = get(url, headers=headers)
    pho = BeautifulSoup(response.content, 'html.parser')

    output = {}
    output['title'] = pho.title.get_text()
    output['body'] = pho.select('div.mk-single-content.clearfix')[0].get_text()
    
    return output
    
def get_articles(urls=BLOG_URLS):
    output = []
    
    for url in urls:
        output.append(get_article(url))

    df = pd.DataFrame(output)
    df.to_csv('codeup_blog.csv')

    return df

def get_all_urls():
    total_pages = 8
    base_url = 'codeup.com/blog/'
    urls = []
    return urls


def get_blog_data(fresh=False):
    if fresh or not os.path.exists('codeup_blog.csv'):
        output = get_articles()
    else:
        output = pd.read_csv('codeup_blog.csv', index_col=0)
    return output

def get_one_topic(url):
    headers = {'user-agent': 'Codeup Bayes Sam'}
    response = get(url, headers=headers)
    mulligatawny = BeautifulSoup(response.content, 'html.parser')

    output = []

    spoonfuls = mulligatawny.select('.news-card')
    for slurp in spoonfuls:
        article = {}
        article['title'] = slurp.select('[itemprop="headline"]')[0].get_text()
        article['content'] = slurp.select('[itemprop="articleBody"]')[0].get_text()
        article['author']  = slurp.select('.author')[0].get_text()
        article['category'] = url.split('/')[-1]
        output.append(article)
    return output

def get_news():
    urls = [
        'https://inshorts.com/en/read/business',
        'https://inshorts.com/en/read/sports',
        'https://inshorts.com/en/read/technology',
        'https://inshorts.com/en/read/entertainment'
        ]
    
    output = []

    for url in urls:
        output.extend(get_one_topic(url))
    news = pd.DataFrame(output)
    news.to_csv('inshort.csv')
    return news

def get_inshort(fresh=False):
    if fresh or not os.path.exists('inshort.csv'):
        inshort = get_news()
    else:
        inshort = pd.read_csv('inshort.csv', index_col=0)
    return inshort
