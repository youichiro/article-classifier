# 記事のカテゴリを分類するDjangoアプリ

## 仕様
- (Gunosyの)記事のURLを入力すると記事のカテゴリを判定し表示します
- カテゴリは[ エンタメ, スポーツ, おもしろ, 国内, 海外, コラム,　IT・科学, グルメ ]です
- ベルヌーイモデルを用いたナイーブベイズ分類器を使って分類します

## 環境
- Python 3.5
- Django 1.10

## 実行
- Gitレポジトリをクローン
`% git clone https://github.com/youichiro/article-classify-app`

- クローンしたレポジトリ "article-classify-app" に移動
`% cd article-classify-app`

- サーバを立てる
`[article-classify-app]% python manage.py runserver`
