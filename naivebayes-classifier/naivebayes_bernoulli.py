# -*- coding:utf-8 -*-
import math
import sys
import os
import random
from collections import defaultdict
from resources.categories import * # 定数の読み込み

"""多項式ベルヌーイモデル"""
class NaiveBayes:
    def __init__(self):
        self.categories = set()   # カテゴリの集合
        self.vocabularies = set() # ボキャブラリの集合
        self.word_count = {}      # word_count[category][word]:カテゴリでの単語の出現回数
        self.category_count = {}  # category_count[category]:カテゴリの出現回数
        self.denominator = {}     # denominator[category]:P(word|category)の分母の値

    def train(self, train_data):
        """ナイーブベイズ分類器の訓練"""
        # 文書集合からカテゴリを抽出して辞書を初期化
        for d in train_data:
            category = d[0]
            self.categories.add(category)
        for c in self.categories:
            self.word_count[c] = defaultdict(int)
            self.category_count[c] = 0
        # 文書集合からカテゴリと単語をカウント
        for d in train_data:
            category, words = d[0], d[1:]
            self.category_count[category] += 1
            for w in words:
                self.vocabularies.add(w)
                self.word_count[category][w] += 1
        # 単語の条件付き確率の分母の値をあらかじめ一括計算しておく
        for c in self.categories:
            self.denominator[c] = sum(self.word_count[c].values()) + len(self.vocabularies)

    def classify(self, test_data):
        """事後確率の対数 log(P(cat|doc)) が最も大きなカテゴリを返す"""
        best = None
        max = -1000000
        for c in self.category_count.keys():
            p = self.score(test_data, c)
            if p > max:
                max = p
                best = c
        return best

    def score(self, words, category):
        """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
        total = sum(self.category_count.values()) # 総文書数
        if self.category_count[category] == 0:
            score = -10.0
        else:
            score = math.log(float(self.category_count[category]) / total) # log P(cat)
        for w in words:
            score += math.log(self.wordProb(w, category)) # log P(word|cat)
        return score

    def wordProb(self, word, category):
        """単語の条件付き確率 P(word|cat) を求める"""
        return float(self.word_count[category][word] + 1) / float(self.denominator[category])


"""ボキャブラリのリストを作る関数"""
def get_vocab(path, category, filename):
    with open(path + category + '/' + filename,'r') as f:
        vocabs = f.readlines()
    vocab_list = []
    for v in vocabs:
        vocab_list.append(v.replace('\n',''))
    return vocab_list

# パスを指定
path = '../data/training_data/'

# 訓練データとテストデータの振り分け
training_data = []
test_data = []
for c in categories:
    file_list = os.listdir(path + c) # データのファイル名を取得
    random.shuffle(file_list)        # 要素をシャッフル
    test_file = file_list[:100]      # 先頭から100個をテストデータに使う
    test_data.append(test_file)
    training_file = file_list[100:]  # 残りを学習データに使う

    # 学習データの作成
    for filename in training_file:
        vocab_list = get_vocab(path, c, filename)
        data = []
        data.append(c)
        for v in vocab_list:
            data.append(v)
        training_data.append(data)

# 学習
cls = NaiveBayes()
cls.train(training_data)

"""
# 学習済み辞書をファイル出力
with open('../learning_result/category_count.txt','w') as f:
    for key, value in cls.category_count.items():
        f.write("{}\t{}\n".format(key,value))

with open('../learning_result/denominator.txt','w') as f:
    for key, value in cls.denominator.items():
        f.write("{}\t{}\n".format(key, value))

with open('../learning_result/word_count.txt','w') as f:
    for key, value in cls.word_count.items():
        for k, v in value.items():
            f.write("{}\t{}\t{}\n".format(key,k,v))
"""

# 分類と評価
total = 0
for c in range(len(test_data)):
    accuracy = 0
    category = categories[c]
    for i in range(len(test_data[c])):
        filename = test_data[c][i]
        test = get_vocab(path, category, filename)
        if cls.classify(test) == category:
            accuracy += 1
    total += accuracy
    print("{}\t{}/100".format(category, accuracy))
print("total: {}".format(total/800))
