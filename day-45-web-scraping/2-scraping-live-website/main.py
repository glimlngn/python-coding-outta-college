from bs4 import BeautifulSoup
import requests
import json

response = requests.get('https://news.ycombinator.com/news').text

soup = BeautifulSoup(response, 'html.parser')
title_list = soup.find_all(name='tr', class_='athing submission')
subtext_list = soup.find_all(name='td', class_='subtext')

article_list = []

for i in range(len(title_list)):
    titleline = title_list[i].find(name='span', class_='titleline')
    title = titleline.getText() # type: ignore
    link = titleline.find('a').get('href') # type: ignore
    try:
        upvotes = int((subtext_list[i].find(name='span', class_='score').getText())[:-7]) # type: ignore
    except AttributeError:
        upvotes = 0

    article_list.append({
        'title': title,
        'link': link,
        'upvotes': upvotes
    })

    print(json.dumps(article_list[i], indent=4))

max_upvotes_article = max(article_list, key=lambda x:x['upvotes'])
print('---\nArticle with the most upvotes:')
print(json.dumps(max_upvotes_article, indent=4))