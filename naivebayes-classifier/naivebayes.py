# -*- coding:utf-8 -*-
import math
import os
from collections import defaultdict
from constants import Categories
from scraping import get_text, get_nouns


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

    def classify(self, article_url):
        """入力された記事URLからカテゴリ分類"""
        text = get_text(article_url)
        nouns = get_nouns(text)
        return self.get_best_category(nouns)

    def get_best_category(self, vocab_list):
        """事後確率の対数 log(P(cat|doc)) が最も大きなカテゴリを返す"""
        best_category = None
        max = -1000000
        for category in self.category_count.keys():
            p = self.get_score(vocab_list, category)
            if p > max:
                max = p
                best_category = category
        return best_category

    def get_score(self, words, category):
        """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
        total = sum(self.category_count.values())   # 総文書数
        if self.category_count[category] == 0:
            score = -10.0
        else:
            score = math.log(float(self.category_count[category]) / total)
        for word in words:
            score += math.log(self.word_prob(word, category))   # log P(word|cat)
        return score

    def word_prob(self, word, category):
        """単語の条件付き確率 P(word|cat) を求める"""
        return float(self.word_count[category][word]+1)/float(self.denominator[category])


def get_vocab(category, filename):
    """ボキャブラリのリストを作る関数"""
    with open('data/'+category+'/'+filename, 'r') as f:
        vocabs = f.readlines()
    vocab_list = []
    for v in vocabs:
        vocab_list.append(v.replace('\n', ''))
    return vocab_list


def make_train_data(train_files):
    """学習データを形成"""
    train_data = []
    for category, filenames in train_files.items():
        for filename in filenames:
            vocab_list = get_vocab(category, filename)
            data = [category]
            for vocab in vocab_list:
                data.append(vocab)
            train_data.append(data)
    return train_data


def main():
    cross_size = 10  # 交差検定の分割数
    # 各カテゴリのデータをcross_size分割する
    split_data = {}
    for category in Categories:
        files = os.listdir('data/'+category.name)
        split_num = len(files) // cross_size
        split_files = []
        for cross in range(cross_size):
            start = split_num * cross
            cross_files = files[start:start+split_num]
            split_files.append(cross_files)
        split_data[category.name] = split_files

    # 10分割交差検定
    for cross in range(cross_size):
        test_files = {}
        train_files = {}

        for category in Categories:
            # cross番目をテストデータにする
            test_files[category.name] = split_data[category.name][cross]
            # それ以外を学習データにする
            flat_train_files = []
            for files in split_data[category.name][0:cross] + split_data[category.name][cross + 1:]:
                for file in files:
                    flat_train_files.append(file)
            train_files[category.name] = flat_train_files

        # 学習データを作成して学習させる
        train_data = make_train_data(train_files)
        nb = NaiveBayes(train_data)
        nb.train()

        # 分類と評価
        accuracy = 0
        article_count = 0
        for category, files in test_files.items():
            for file_name in files:
                #print(str(category)+str(file_name))
                test_vocab_list = get_vocab(category, file_name)
                result = nb.get_best_category(test_vocab_list)
                print("result: {}\tans: {}".format(result, category))
                if result == category:
                    accuracy += 1
                article_count += 1
        print("cross: {}\taccuracy: {}%".format(cross + 1, accuracy / article_count * 100))


"""
        # 分類と評価
        total = 0
        count_file = 0
        for c in range(len(test_data)):
            accuracy = 0
            category = CATEGORIES[c]
            for i in range(len(test_data[c])):
                filename = test_data[c][i]
                test = get_vocab(category, filename)
                if cls.classify_test(test) == category:
                    accuracy += 1
                count_file += 1
            total += accuracy
        print("cross: {}\taccuracy: {}".format(cross + 1, total / count_file))
"""

if __name__ == '__main__':
    main()
