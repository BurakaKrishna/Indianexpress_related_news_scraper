# -*- coding: utf-8 -*-

# ------- imports -------
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import threading
import requests
import time
import sys
import re
from collections import defaultdict
import pandas as pd

# ------- Global variables -------
DAY = str(datetime.date(datetime.now()))
DB = {}
VISITED = defaultdict(list)
CHAT_ID = -0    # int, channel ID
RAGHAV_ID = 0   # int, account ID
TOKEN = 'token of a bot'
TOMORROW = ['front_page', 'editorials', 'opinion', 'explained']
LINKS = {
    'front_page': 'https://indianexpress.com/print/front-page/feed/',
    'lifestyle': 'https://indianexpress.com/section/refreshlifestyle/feed/',
    'health': 'https://indianexpress.com/section/lifestyle/health/feed/',
    'science_tech': 'https://indianexpress.com/section/technology/feed/',
    'hockey': 'https://indianexpress.com/section/sports/hockey/feed/',
    'cricket': 'https://indianexpress.com/section/sports/cricket/feed/',
    'sports': 'https://indianexpress.com/section/sports/feed/',
    'economy': 'https://indianexpress.com/section/business/feed/',
    'india': 'https://indianexpress.com/section/india/feed/',
    'world': 'https://indianexpress.com/section/world/feed/',
    # 'eye': 'https://indianexpress.com/print/eye/feed/',
    # 'opinion': 'https://indianexpress.com/section/opinion/feed/',
    # 'explained': 'https://indianexpress.com/section/explained/feed/',
    # 'editorials': 'https://indianexpress.com/section/opinion/editorials/feed/',
    'politics': 'https://indianexpress.com/section/india/politics/feed/',
}


def fetch_related_articles(entry):
    target_article = entry['link']
    response = requests.get(target_article)
    soup = BeautifulSoup(response.text, 'html.parser')
    related_articles = soup.find_all(class_='m-article-small__title')
    results = {}
    if len(related_articles) >=1:
     for article in related_articles:
         results[article.a.get('title')] = article.a.get('href')
    return results


# ------- Insert new feeds(by editing the message) -------
def rss_feed():
    articles = {}
    for link_key in LINKS:
        print('\n', '-' * 10, link_key, '-' * 10)
        xml = feedparser.parse(LINKS[link_key])
        # count = 0
        for entry in xml.entries:
            entry_id = int(re.split('&p=', entry['id'])[1])
            if entry_id not in VISITED[link_key]:
                print(f"{datetime.now().strftime('%I:%M %p')} | {entry.title[:50]}")
                related_articles = fetch_related_articles(entry)
                articles[entry.title] = {'related_articles':related_articles,'link':entry['link'],'category':link_key}
                VISITED[link_key].append(entry_id)
            #     count += 1
            # if count == 5:
            #     break
    article_df = pd.DataFrame(list(articles.items()))
    article_df.to_csv('Related_articles_for_day_'+str(DAY))



print (rss_feed())
#
# while True:
#     try:
#             rss_thread = threading.Thread(target=rss_feed,)
#             rss_thread.start()
#             time.sleep(30 * 60)
#     except Exception as e:
#         print(e)
#         time.sleep(30 * 60)
