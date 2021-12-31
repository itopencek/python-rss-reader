import os
import tempfile

import pandas as pd
import pytest
from flask import render_template

from ArticleParserApp import main, create_database, app, db

# Testing controllers with their services - simple integration tests
from ArticleParserApp.services.stats import get_num_of_articles, get_most_recent_articles, get_most_used_words, \
    get_contains, num_of_articles_by_sites


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = main({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            create_database()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_index(client):
    post_site(client)

    rv = client.get('/')
    assert bytes(render_template('index.html', articles=None,
                                 data={'max': 0, 'limit': 5, 'page': 1}), 'utf-8') == rv.data


def test_add_site(client):
    rv = client.get('/add-site')

    assert bytes(render_template('add-site.html'), 'utf-8') == rv.data


def test_sites(client):
    post_site(client)

    rv = client.get('/sites')

    assert bytes(render_template('sites.html', sites=[{
        'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'
    }]), 'utf-8') == rv.data


def test_stats(client):
    post_site(client)

    rv = client.get('/stats')

    assert bytes(render_template('stats.html', words=[], articles=[]), 'utf-8') == rv.data


def test_sites(client):
    rv_post = post_site(client)
    assert b'"status":200' in rv_post.data

    rv = client.get('/api/site/test')
    assert b'"name":"test"' in rv.data
    assert b'"id":1' in rv.data
    assert b'"url":"https://www.sme.sk/rss-title"' in rv.data
    assert b'"description":"Test description."' in rv.data
    assert b'"language":"sk"' in rv.data


def test_sites_exception(client):
    rv_post = client.post('/api/site')

    assert b'{"message":"Wrong or missing parameter","parameter":"site","status":400}\n' == rv_post.data


def test_delete_site(client):
    rv_post = post_site(client)
    assert b'"status":200' in rv_post.data

    # delete site
    rv = client.delete('/api/site/delete/1')

    assert b'"status":200' in rv.data

    # can't delete the same site again
    rv = client.delete('/api/site/delete/1')

    assert b'{"message":"Wrong or missing parameter","parameter":"site_id","status":400}\n' == rv.data


def test_delete_site_exception(client):
    rv_post = client.delete('/api/site/delete/asd')

    assert b'{"message":"Wrong or missing parameter","parameter":"site_id","status":400}\n' == rv_post.data


def test_get_site(client):
    rv_post = post_site(client)

    assert b'"status":200' in rv_post.data

    rv = client.get('/api/site/test')

    assert b'"name":"test"' in rv.data
    assert b'"id":1' in rv.data
    assert b'"url":"https://www.sme.sk/rss-title"' in rv.data
    assert b'"description":"Test description."' in rv.data
    assert b'"language":"sk"' in rv.data


def test_site_empty(client):
    client.post('/api/site')

    rv = client.get('/api/site/test')
    assert b'{"message":"Wrong or missing parameter","parameter":"name","status":400}\n' in rv.data


def post_site(client):
    return client.post('/api/site', json={
        'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'
    })


# Testing services

def test_get_num_of_articles_zero(client):
    result = get_num_of_articles()

    assert result == 0


def get_df_with_article():
    article = {'id': 1, 'url': 'test.url', 'name': 'test-name', 'description': 'test desc',
               'image_url': 'test image_url', 'date': '123456789', 'site_id': 1}
    site = {'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'}
    with app.app_context():
        df_article = pd.read_sql('SELECT * FROM article', con=db.engine)
        df_site = pd.read_sql('SELECT * FROM site', con=db.engine)
    df_article = df_article.append([article])
    df_site = df_site.append([site])
    return df_article, df_site


def test_get_num_of_articles(client):
    post_site(client)
    df_article, df_site = get_df_with_article()

    result = get_most_recent_articles(df=df_article, df_s=df_site)

    assert str(result) == "[{'id_x': 1, 'url_x': 'test.url', 'name_x': 'test-name', 'description_x': 'test desc', " \
                          "'image_url': 'test image_url', 'date': Timestamp('1973-11-29 22:33:09'), 'site_id': 1, " \
                          "'id_y': 1.0, 'name_y': 'test', 'url_y': 'https://www.sme.sk/rss-title', 'description_y': " \
                          "'Test description.', 'language': 'sk'}]"


def test_get_most_used_words(client):
    post_site(client)
    df_article, df_site = get_df_with_article()

    result = get_most_used_words(df=df_article, exclude=False)

    assert str(result) == "{'test-name': 1}"


def test_get_contains(client):
    post_site(client)
    df_article, df_site = get_df_with_article()

    result = str(get_contains('test-name', df=df_article))

    assert 'test-name' in result
    assert 'test.url' in result
    assert '123456789' in result
    assert 'test desc' in result


def test_num_of_articles_by_sites(client):
    post_site(client)
    df_article, df_site = get_df_with_article()

    result = num_of_articles_by_sites(df=df_article, df_s=df_site)

    assert str(result) == "[['test' 1]]"
