# -*- coding: utf-8 -*-
import math, sys, os, random
from collections import defaultdict
from resources.categories import * # 定数の読み込み

class Feature:
    """Feature for NaiveBayes"""
    def __init__(self,name):
        self.name = name
        self.categories = defaultdict(int)
    def __getitem__(self,category):
        return self.categories[category]
    def __setitem__(self,category,value):
        self.categories[category] = value

class NaiveBayesClassifier:
    """ NaiveBayes """
    def __init__(self):
        self.categories = defaultdict(int)
        self.features = {}
        self.training_count = 0
        self.alpha = 1

    def learn(self,category,features):
        self.categories[category] += 1  # カテゴリをカウント
        for f in features:
            if f not in self.features:
                self.features[f] = Feature(f)
            self.features[f][category] += 1
    
    def classify(self,features):
        result = None
        max_score = 0
        
        if len(features) == 0:
            return result

        for c in self.categories:
            score = float(self.categories[c] + self.alpha) / (self.training_count + len(self.categories) * self.alpha)
            for f in features:
                if f not in self.features.keys():
                    score *= self.alpha / (self.categories[c] + 2 * self.alpha)
                else:
                    score *= (self.features[f][c] + self.alpha) / (self.categories[c] + 2 * self.alpha)
            if max_score < score:
                result, max_score = c, score
        return result


def get_feature(path, category, filename):
    """要素のリストを作る"""
    with open(path + category + '/' + filename,'r') as f:
        features = f.readlines()
    feature_list = []
    for f in features:
        feature_list.append(f.replace('\n',''))
    return feature_list

# パスを指定
path = '../data/training_data/'

training_data = []
test_data = []

for c in range(len(categories)):
    # ファイルの名前を取得
    file_list = os.listdir(path + categories[c])
    # 要素をシャッフル
    random.shuffle(file_list)

    # 前から100個をテストデータに使う
    test_file = file_list[:100]
    test_data.append(test_file)
    # 残りを学習データに使う
    training_file = file_list[100:]

    # 学習データの作成
    for filename in training_file:
        feature_list = get_feature(path, categories[c], filename)
        data = []
        data.append(categories[c])
        data.append(feature_list)
        training_data.append(data)

cls = NaiveBayesClassifier()

# 学習
for c, f in training_data:
    cls.learn(c,f)

# 分類
total = 0
for c in range(len(test_data)):
    category = categories[c]
    accuracy = 0
    for i in range(len(test_data[c])):
        filename = test_data[c][i]
        if cls.classify(get_feature(path, category, filename)) == category:
            accuracy += 1
    total += accuracy
    print("{}\t{}/100".format(category, accuracy))
print("total: {}".format(total/800))
