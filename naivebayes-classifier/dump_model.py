import pickle
import os
from resources.categories import categories
from naivebayes_bernoulli import NaiveBayes, make_traindata

"""学習モデルのインスタンスをpickle形式で保存"""
if __name__ == '__main__':
    path = 'data/training_data/'
    file_list = []
    for c in categories:
        files = os.listdir(path + c)
        file_list.append(files)

    training_data = []
    for i in range(len(categories)):
        training = [categories[i]]
        for f in file_list[i]:
            training.append(f)
        training_data.append(training)

    train_data = make_traindata(training_data)
    cls = NaiveBayes(train_data)

    with open('resources/model.pkl', 'wb') as f:
        pickle.dump(cls, f)
