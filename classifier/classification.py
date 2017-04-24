# -*- coding: utf-8 -*-
import math
import lxml.html
import requests
import MeCab
import os
from collections import defaultdict

class NaiveBayes:
    """ベルヌーイモデルによる分類"""
    def __init__(self):
        self.word_count = {}
        self.category_count = {}
        self.denominator = {}
        self.remake_dict() # 辞書復元

    def remake_dict(self):
        """学習済み辞書の復元"""
        path = os.path.abspath(".") + "/classifier" # カウントディレクトリ
        # category_countの復元
        with open(path+'/data/category_count.txt','r') as f:
            category_data = f.readlines()
        for line in category_data:
            element = line.replace('\n','').split('\t')
            self.category_count[element[0]] = int(element[1])
        # denominatorの復元
        with open(path+'/data/denominator.txt','r') as f:
            denominator_data = f.readlines()
        for line in denominator_data:
            element = line.replace('\n','').split('\t')
            self.denominator[element[0]] = int(element[1])
        # word_countの復元
        for c in self.category_count.keys():
            self.word_count[c] = defaultdict(int)
        with open(path+'/data/word_count.txt','r') as f:
            word_data = f.readlines()
        for line in word_data:
            element = line.replace('\n','').split('\t')
            self.word_count[element[0]][element[1]] = int(element[2])
                
    def scraping(self, target_url):
        """URLからHTMLを読み込み、本文を抽出する関数"""
        target_html = requests.get(target_url).text
        root = lxml.html.fromstring(target_html)
        article_text = root.xpath('//div[@class="article gtm-click"]/p/text()')
        return article_text

    def mecab(self, article_text):
        """テキストから名詞を抽出する関数"""
        tagger = MeCab.Tagger('Ochasen')
        tagger.parse('') # エラー回避のため
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

    def wordProb(self, word, category):
        return float(self.word_count[category][word]+1) / float(self.denominator[category])

