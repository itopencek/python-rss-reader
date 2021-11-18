from src.controllers.exceptions import exception
from src.controllers.views import views
from src.controllers.api import api
from src.parser.rssparser import RssParser
from src.reader.webreader import WebReader
from flask import Flask

app = Flask(__name__)


def register_blueprints():
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')


def register_exceptions():
    app.register_blueprint(exception)


def get_articles(url):
    parser = RssParser()
    reader = WebReader()
    website = reader.read(url)
    return parser.parse(website).values


def main():
    register_exceptions()
    register_blueprints()
    data = get_articles("https://www.sme.sk/rss-title")
    print("Started application.")
    return app
