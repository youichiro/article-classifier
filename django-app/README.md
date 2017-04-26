# 記事のカテゴリを分類するDjangoアプリ

## 仕様
- Gunosyのwebニュース記事のURLを入力すると記事のカテゴリを判定し表示する
- カテゴリは[ エンタメ, スポーツ, おもしろ, 国内, 海外, コラム, IT・科学, グルメ ]

## 環境
- Python 3.5
- Django 1.10

## その他必要なモジュール
- math
- lxml
- requests
- MeCab
- os

## 実行
- Gitレポジトリをクローン
`% git clone https://github.com/youichiro/article-classify-app`

- クローンしたレポジトリ "article-classify-app" に移動
`% cd article-classify-app`

- Djangoのレポジトリに "django-app" 移動
`[article-classify-app]% cd django-app`

- サーバを立てる
`[article-classify-app/django-app]% python manage.py runserver`

- 各種必要なモジュールをインポートする場合
`pip install <モジュール名>`
