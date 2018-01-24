from django.shortcuts import render
from .form import UrlForm
import os
import sys
import pickle

sys.path.append(os.path.abspath(".") + '/../naivebayes-classifier')

# 学習モデルを読み込む
path = os.path.abspath("../naivebayes-classifier/resources")
with open(path+'/model.pkl', 'rb') as f:
    nb = pickle.load(f)
nb.train()


def form(request):
    form_style = UrlForm()
    category = ""

    if request.POST:
        post_url = request.POST['url']
        category_en = nb.classify(post_url)
        if category_en == "column":
            category = "コラム"
        elif category_en == "overseas":
            category = "海外"
        elif category_en == "funny":
            category = "おもしろ"
        elif category_en == "domestic":
            category = "国内"
        elif category_en == "sports":
            category = "スポーツ"
        elif category_en == "gourment":
            category = "グルメ"
        elif category_en == "entertainment":
            category = "エンタメ"
        elif category_en == "it_science":
            category = "IT・科学"
        else:
            category = ""

    return render(request, 'classifier/form.html', {'form_style': form_style, 'category': category})

