import pickle
import os
from constants import CATEGORIES
from naivebayes import NaiveBayes, make_train_data

"""学習モデルのインスタンスをpickle形式で保存"""
if __name__ == '__main__':
    train_files = {}
    for category in CATEGORIES:
        files = os.listdir('data/' + category)
        train_files[category] = files

    train_data = make_train_data(train_files)
    nb = NaiveBayes(train_data)

    with open('resources/model.pkl', 'wb') as f:
        pickle.dump(nb, f)
