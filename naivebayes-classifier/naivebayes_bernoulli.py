# -*- coding:utf-8 -*-
import math
import os
import lxml.html
import requests
import MeCab
from collections import defaultdict
from resources.categories import categories  # 定数の読み込み


class NaiveBayes:
    """多項式ベルヌーイモデル"""
    def __init__(self, train_data):
        self.train_data = train_data
        self.categories = set()     # カテゴリの集合
        self.vocabularies = set()   # ボキャブラリの集合
        self.word_count = {}        # カテゴリでの単語の出現回数
        self.category_count = {}    # カテゴリの出現回数
        self.denominator = {}       # P(word|category)の分母の値

    def train(self):
        """ナイーブベイズ分類器の訓練"""
        # 文書集合からカテゴリを抽出して辞書を初期化
        for d in self.train_data:
            category = d[0]
            self.categories.add(category)
        for c in self.categories:
            self.word_count[c] = defaultdict(int)
            self.category_count[c] = 0
        # 文書集合からカテゴリと単語をカウント
        for d in self.train_data:
            category, words = d[0], d[1:]
            self.category_count[category] += 1
            for w in words:
                self.vocabularies.add(w)
                self.word_count[category][w] += 1
        # 単語の条件付き確率の分母の値をあらかじめ一括計算しておく
        for c in self.categories:
            self.denominator[c] = sum(self.word_count[c].values()) + len(self.vocabularies)

    def classify_test(self, test_data):
        """事後確率の対数 log(P(cat|doc)) が最も大きなカテゴリを返す"""
        best = None
        max = -1000000
        for c in self.category_count.keys():
            p = self.score(test_data, c)
            if p > max:
                max = p
                best = c
        return best

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

    def scraping(self, target_url):
        """URLからHTMLを読み込み、本文を抽出する関数"""
        target_html = requests.get(target_url).text
        root = lxml.html.fromstring(target_html)
        article_text = root.xpath('//div[@class="article gtm-click"]/p/text()')
        return article_text

    def mecab(self, article_text):
        """テキストから名詞を抽出する関数"""
        tagger = MeCab.Tagger('Ochasen')
        tagger.parse('')
        node = tagger.parseToNode(article_text)
        noun_list = []
        while node:
            if node.feature.split(',')[0] == '名詞':
                noun_list.append(node.surface)
            node = node.next
        return noun_list

    def score(self, words, category):
        """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
        total = sum(self.category_count.values())   # 総文書数
        if self.category_count[category] == 0:
            score = -10.0
        else:
            score = math.log(float(self.category_count[category]) / total)
        for w in words:
            score += math.log(self.wordProb(w, category))   # log P(word|cat)
        return score

    def wordProb(self, word, c):
        """単語の条件付き確率 P(word|cat) を求める"""
        return float(self.word_count[c][word]+1)/float(self.denominator[c])


def get_vocab(category, filename):
    """ボキャブラリのリストを作る関数"""
    with open(path + category + '/' + filename, 'r') as f:
        vocabs = f.readlines()
    vocab_list = []
    for v in vocabs:
        vocab_list.append(v.replace('\n', ''))
    return vocab_list


def make_traindata(training_data):
    """学習データを形成"""
    train_data = []
    for c in training_data:
        category = c[0]
        for filename in c[1:]:
            vocab_list = get_vocab(category, filename)
            data = [category]
            for v in vocab_list:
                data.append(v)
            train_data.append(data)
    return train_data


if __name__ == '__main__':
    
    # パスを指定
    path = 'data/training_data/'

    # 交差検定の分割数
    cross_size = 10
    
    # 各カテゴリファイルの分割するファイル数
    file_list = []
    split_num = []
    for c in categories:
        files = os.listdir(path + c)
        file_list.append(files)
        split = len(files) // cross_size
        split_num.append(split)

    # 10分割交差検定
    for cross in range(cross_size):
        test_data = []
        training_data = []
    
        for i in range(len(categories)):
            # fileを10分割したリストを作成
            slices = []
            for s in range(0, len(file_list[i]), split_num[i]):
                slices.append(file_list[i][s:s+split_num[i]])
    
            # cross番目をテストデータにする
            test_data.append(slices[cross])
    
            # cross番目以外を学習データにする
            training = [categories[i]]
            for s in slices:
                if s == slices[cross]:
                    pass
                else:
                    for f in s:
                        training.append(f)
            training_data.append(training)
    
        # 学習データを形成
        train_data = make_traindata(training_data)
        cls = NaiveBayes(train_data)
        cls.train()
    
        # 分類と評価
        total = 0
        count_file = 0
        for c in range(len(test_data)):
            accuracy = 0
            category = categories[c]
            for i in range(len(test_data[c])):
                filename = test_data[c][i]
                test = get_vocab(category, filename)
                if cls.classify_test(test) == category:
                    accuracy += 1
                count_file += 1
            total += accuracy
        print("cross: {}\taccuracy: {}".format(cross + 1, total / count_file))
