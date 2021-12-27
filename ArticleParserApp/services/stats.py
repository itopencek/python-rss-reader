import pandas as pd

from ArticleParserApp import df_articles
from ArticleParserApp.database.models.models import Article


def get_most_recent_articles(num):
    """
    Returns most recent articles up to the given number.
    :param num: num of articles to get
    :return: articles
    """
    return Article.query.order_by(Article.date).limit(num).all()


def get_most_used_words():
    """
    Returns 5 most used words in article names (titles).
    :return: 5 most used words
    """
    most_used = pd.Series(' '.join(df_articles['name']).lower().split()).value_counts()[:5]
    return most_used


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
    return df_articles.groupby(['site_id']).size().to_frame('articles').reset_index()
