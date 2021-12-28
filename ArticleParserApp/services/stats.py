from datetime import datetime

import pandas as pd

from ArticleParserApp import df_articles, df_sites
from ArticleParserApp.database.models.models import Article


def get_most_recent_articles(num):
    """
    Returns most recent articles up to the given number.
    :param num: num of articles to get
    :return: articles
    """
    articles = Article.query.order_by(Article.date.desc()).limit(num).all()
    for article in articles:
        article.set_date(datetime.fromtimestamp(int(article.get_date())))
    return articles


def get_most_used_words():
    """
    Returns 5 most used words in article names (titles).
    :return: 5 most used words as dictionary with number of times used
    """
    most_used = pd.Series(' '.join(df_articles['name']).lower().split()).value_counts()[:5]
    most_used_dict = dict(zip(most_used.index, most_used))
    return most_used_dict


def get_contains(word, case=False):
    """
    Returns articles, which contain given word.
    :param word: word the articles should contain
    :param case: if the search should be case-sensitive
    :return: articles
    """
    return df_articles[df_articles.name.str.contains(word, case=case)]


def num_of_articles_by_sites():
    """
    Returns number of articles per site, which are in database.
    :return:
    """
    joined_tables = pd.merge(df_articles, df_sites, left_on='site_id', right_on='id')
    articles = joined_tables.groupby(['name_y']).size().to_frame('articles').reset_index()
    return articles.values
