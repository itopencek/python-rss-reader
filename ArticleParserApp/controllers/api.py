from flask import Blueprint, jsonify, request

from ArticleParserApp.database.models.exceptions.api import WrongParamException
from ArticleParserApp.database.models.models import Site, Article
from ArticleParserApp import db, RssParser
from ArticleParserApp.parser.reader import WebReader

api = Blueprint('api', __name__)


@api.route('/articles/<name>', methods=['GET'])
def get_articles(name):
    """
    Returns articles for given site name.
    Site must be already in database. Otherwise, WrongParamException is raised.
    :param name: site name to get articles from
    :return: articles
    """
    site = Site.query.filter_by(name=name).first()
    if site is None:
        raise WrongParamException('name')

    parsed = parse_articles(site.url)
    return jsonify(parsed), 200


@api.route('/articles/<name>', methods=['PUT'])
def save_articles(name):
    """
    Saves articles from site to database.
    :param name: site name to use
    """
    site = Site.query.filter_by(name=name).first()
    if site is None:
        raise WrongParamException('name')

    articles = parse_articles(site.url)
    for article in articles:
        if Article.query.filter_by(name=article['title']).first():
            print("Had to skip article with name \"" + article['title'] + "\", because it already exists!")
        else:
            new_article = Article().from_parsed(article, site.id)
            db.session.add(new_article)
    db.session.commit()
    return jsonify(site.as_dict()), 200


@api.route('/site/<name>', methods=['GET'])
def get_site(name):
    site = Site.query.filter_by(name=name).first()
    if site is None:
        raise WrongParamException('name')

    return jsonify(site.as_dict()), 200


@api.route('/site', methods=['POST'])
def post_site():
    """
    Adds site to database.
    Must be valid.
    :return:
    """
    body = request.get_json()

    if body == "":
        raise WrongParamException('website')

    website = Site(name=body['name'], url=body['url'], description=body['description'])
    db.session.add(website)
    db.session.commit()

    return return_status(200)


def return_status(status):
    return jsonify(status=status), 200


def parse_articles(url):
    html = WebReader().read(url)
    return RssParser().parse(html)
