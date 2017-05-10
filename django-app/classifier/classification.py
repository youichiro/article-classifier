# -*- coding: utf-8 -*-
import math
import lxml.html
import requests
import MeCab
import os
from collections import defaultdict
import pickle


class NaiveBayes:
    """ベルヌーイモデルによる分類"""
    def __init__(self):
        self.word_count = {}
        self.category_count = {}
        self.denominator = {}
        self.load_dict()    # 辞書復元

    def load_dict(self):
        """学習済み辞書の復元"""
        path = os.path.abspath(".") + "/classifier"     # カウントディレクトリのパス
        with open(path+'/data/category_count.pkl', 'rb') as f:
            self.category_count = pickle.load(f)
        with open(path+'/data/denominator.pkl', 'rb') as f:
            self.denominator = pickle.load(f)
        with open(path+'/data/word_count.pkl', 'rb') as f:
            self.word_count = pickle.load(f)

    def scraping(self, target_url):
        """URLからHTMLを読み込み、本文を抽出する関数"""
        target_html = requests.get(target_url).text
        root = lxml.html.fromstring(target_html)
        article_text = root.xpath('//div[@class="article gtm-click"]/p/text()')
        return article_text

    def mecab(self, article_text):
        """テキストから名詞を抽出する関数"""
        tagger = MeCab.Tagger('Ochasen')
        tagger.parse('')    # エラー回避のため
        node = tagger.parseToNode(article_text)
        noun_list = []
        while node:
            if node.feature.split(',')[0] == '名詞':
                noun_list.append(node.surface)
            node = node.next
        return noun_list

    def classify(self, target_url):
        """URLから記事のカテゴリを分類"""
        # 本文抽出
        article_text = ''.join(self.scraping(target_url))
        # 名詞抽出
        article_data = self.mecab(article_text)

        # 確率が最大となるカテゴリを求める
        best = None
        max = -1000000
        for c in self.category_count.keys():
            p = self.score(article_data, c)
            if p > max:
                max = p
                best = c
        return best

    def score(self, words, category):
        """確率を計算"""
        total = sum(self.category_count.values())
        if self.category_count[category] == 0:
            score = -10.0
        else:
            score = math.log(float(self.category_count[category]) / total)
        for word in words:
            score += math.log(self.wordProb(word, category))
        return score

    def wordProb(self, word, c):
        over = self.word_count[c][word] + 1
        under = self.denominator[c]
        return float(over / under)
