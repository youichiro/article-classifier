# 記事のカテゴリ分類器

## 概要
- Webニュース記事のURLを入力するとその記事のカテゴリを予測する分類器を実装した
- 分類するカテゴリーは[ エンタメ, スポーツ, おもしろ, 国内, 海外, コラム, IT・科学, グルメ ]とした
- GunosyのWebニュース記事をスクレイピングして学習データとして利用した

## 分類器アプリ
### 環境
- Python 3.5
- Django 1.10

### 使い方
- `git clone https://github.com/youichiro/article-classify-app`
- `cd article-classify-app/django-app`
- `pip install -r requirements.txt`
- `python manage.py runserver`

