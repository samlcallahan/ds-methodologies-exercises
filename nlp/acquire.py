from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_article(url):
    headers = {'user-agent': 'Codeup Bayes Sam'}
    response = get(url, headers=headers)
    pho = BeautifulSoup(response.content, 'html.parser')

    title = pho.title.get_text()
    body = pho.select('div.mk-single-content.clearfix')[0].get_text()
    
    return {
        "title": title,
        "body": body
    }

def get_articles():
    urls = [
        "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
        "https://codeup.com/data-science-myths/",
        "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
        "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
        "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/",
    ]

    output = []
    
    for url in urls:
        output.append(get_article(url))

    df = pd.DataFrame(output)
    df.to_csv('codeup_blog.csv')

    return df

def get_blog_data(fresh=False):
    if fresh or not os.path.exists('codeup_blog.csv'):
        output = get_articles()
    else:
        output = pd.read_csv('codeup_blog.csv')
    return output

blogs = get_blog_data(True)