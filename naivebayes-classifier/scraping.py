"""ニュース記事をスクレイピングして名詞を抽出して保存する"""

# -*- coding:utf-8 -*-
import os
import lxml.html
import requests
import MeCab
from tqdm import tqdm
from constants import Categories


def get_article_urls(target_url):
    """ページに配置されている記事のURLを取得する"""
    target_html = requests.get(target_url).text
    root = lxml.html.fromstring(target_html)
    articles = root.xpath('//div[@class="list_title"]/a')
    url_list = []
    for article in articles:
        url_list.append(article.attrib['href'])
    return url_list


def get_article_text(article_url):
    """記事から本文を抽出する"""
    article_html = requests.get(article_url).text
    root = lxml.html.fromstring(article_html)
    article_text = root.xpath('//div[@class="article gtm-click"]/p/text()')
    return ''.join(article_text)


def get_article_nouns(article_text):
    """本文から名詞を抽出する"""
    # neologdを使う
    # https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
    tagger = MeCab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    node = tagger.parseToNode(article_text)
    noun_list = []
    while node:
        if node.feature.split(',')[0] == '名詞':
            noun_list.append(node.surface)
        node = node.next
    return noun_list


def save_nouns_to_textfile(category, number, nouns):
    """名詞集合をテキストファイルに保存する"""
    # ディレクトリが存在しない場合 mkdir
    if not os.path.exists('./data/'+category):
        os.mkdir('./data/'+category)
    # ex. data/sports/article_3.txt
    with open('data/'+category+'/article_'+str(number+1)+'.txt', 'w') as f:
        for noun in nouns:
            f.write(noun+'\n')


def main():
    base_url = 'https://gunosy.com/categories/'

    # 記事のURLを収集する
    print("scraping url")
    all_url = {}
    for category in Categories:
        print(category.name)
        url_list = []
        for page in tqdm(range(5)):
            target_url = base_url + str(category.value) + '?page=' + str(page + 1)
            url_list.extend((get_article_urls(target_url)))
        all_url[category.name] = url_list

    # 記事の本文を取得し、名詞のみを抽出してテキストファイルに保存する
    print("scraping text")
    for category, article_urls in all_url.items():
        print(category)
        for number, article_url in enumerate(tqdm(article_urls)):
            text = get_article_text(article_url)
            nouns = get_article_nouns(text)
            save_nouns_to_textfile(category, number, nouns)


if __name__ == '__main__':
    main()
