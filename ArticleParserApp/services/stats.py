import pandas as pd

from ArticleParserApp import df_articles
from ArticleParserApp.database.models.models import Article


def get_most_recent_articles(num):
    return Article.query.order_by(Article.date).limit(num).all()


def get_most_used_words():
    most_used = pd.Series(' '.join(df_articles['name']).lower().split()).value_counts()[:5]
    return most_used


def get_contains(word, case=False):
    return df_articles[df_articles.name.str.contains(word, case=case)]


def num_of_articles_by_sites():
    return df_articles.groupby(['site_id']).size().to_frame('articles').reset_index()
