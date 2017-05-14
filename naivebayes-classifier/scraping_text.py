# -*- coding:utf-8 -*-
import lxml.html, requests
from resources.categories import * # 定数の読み込み

"""記事から本文を抽出し、ファイルに出力する関数"""
def get_text(target_url, category, number):
    # 本文を抽出
    target_html = requests.get(target_url).text
    root = lxml.html.fromstring(target_html)
    article_text = root.xpath('//div[@class="article gtm-click"]/p/text()')
    # ファイル出力
    f1 = open('../data/texts/'+category+'/'+category+str(number)+'.txt','w')
    for text in article_text:
        f1.write(text+'\n')
    f1.close()


for category in categories:
    print(category)
    # カテゴリの記事URLを読み込む
    f2 = open('../data/urls/'+category+'_urls.txt','r')
    urls = f2.readlines()
    f2.close()
    number = 0
    # 記事のURLから本文を抽出し、ファイルに書き込む
    for target_url in urls:
        number += 1
        print(category+str(number))
        get_text(target_url.replace('\n',''), category, number)
