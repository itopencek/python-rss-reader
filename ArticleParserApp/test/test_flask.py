import os
import tempfile

import pytest
from flask import render_template

from ArticleParserApp import main, create_database


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
    client.post('/api/site', json={
        'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'
    })

    rv = client.get('/')
    assert bytes(render_template('index.html', articles=[
        {'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'}],
                                 data={'max': 0, 'limit': 5, 'page': 1}), 'utf-8') in rv.data


def test_sites(client):
    rv_post = client.post('/api/site', json={
        'name': 'test', 'url': 'https://www.sme.sk/rss-title', 'description': 'Test description.', 'language': 'sk'
    })
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
