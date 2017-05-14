# -*- coding:utf-8 -*-
"""
記事一覧ページから各記事のURLを抽出する
"""
import lxml.html
import requests
from resources.categories import * # 定数の読み込み

def get_URLs(target_url):
    # ニュースの記事を所得する
    target_html = requests.get(target_url).text
    root = lxml.html.fromstring(target_html)
    article_url = root.xpath('//div[@class="list_title"]/a')
    url_list = []
    for i in range(len(article_url)):
        url_list.append(article_url[i].attrib['href'])
    return url_list


# カテゴリごとのURLを取得し、ファイルに書き込む
for category in range(len(categories)):
    print(categories[category])
    url_list = []
    for page in range(100):
        print(page+1)
        url_list.extend(get_URLs('https://gunosy.com/categories/' + str(category+1) + '?page=' + str(page+1)))
    f = open('../data/'+categories[category]+'_urls.txt','w')
    for line in url_list:
        f.write(line + '\n')
    f.close
