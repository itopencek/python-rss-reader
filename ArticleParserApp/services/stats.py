from datetime import datetime

import numpy as np
import pandas as pd

from ArticleParserApp import df_articles, df_sites


def get_num_of_articles(df=df_articles):
    """
    Returns number of articles in database or if the number is greater than 35, returns 35.
    """
    try:
        if df.shape[0] > 35:
            return 35
        else:
            return df.shape[0]
    except AttributeError:
        return 0


def get_most_recent_articles(limit=5, offset=0, df=df_articles, df_s=df_sites):
    """
    Returns most recent articles up to the given number.
    :param df_s: dataframe for sites
    :param df: dataframe to use for articles
    :param limit: max number of articles
    :param offset: offset articles
    :return: articles
    """
    if df is None or len(df) == 0:
        return

    joined_tables = pd.merge(df, df_s, left_on='site_id', right_on='id') \
        .sort_values('date', ascending=False).iloc[offset:limit + offset]

    # convert date to readable format
    joined_tables['date'] = joined_tables['date'].apply(lambda date: datetime.fromtimestamp(int(date)))
    return joined_tables.to_dict('records')


def get_most_used_words(df=df_articles, exclude=True):
    """
    Returns 5 most used words in article names (titles).
    :return: 5 most used words as dictionary with number of times used
    """
    if df is None or len(df) == 0:
        return []

    most_used = pd.Series(' '.join(df['name']).lower().split()).value_counts()
    if exclude:
        excluded_words = get_excluded_words()
    else:
        excluded_words = []
    most_used = most_used.loc[~np.in1d(most_used.index.values, excluded_words)][:5]
    most_used_dict = dict(zip(most_used.index, most_used))
    return most_used_dict


def get_contains(word, df=df_articles, case=False):
    """
    Returns articles, which contain given word.
    :param df: dataframe for articles
    :param word: word the articles should contain
    :param case: if the search should be case-sensitive
    :return: articles
    """
    return df[df.name.str.contains(word, case=case)]


def num_of_articles_by_sites(df=df_articles, df_s=df_sites):
    """
    Returns number of articles per site, which are in database.
    """
    if df is None or len(df) == 0:
        return []

    joined_tables = pd.merge(df, df_s, left_on='site_id', right_on='id')
    articles = joined_tables.groupby(['name_y']).size().to_frame('articles').reset_index()
    return articles.values


def get_excluded_words():
    """
    Returns list of words, which should not be in most used words.
    Reads list from file database/excluded-words.txt.
    """
    with open("database/excluded-words.txt", "r") as f:
        words = [x[:-1] for x in f.readlines()]

    return words
