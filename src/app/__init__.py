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


def main():
    register_exceptions()
    register_blueprints()
    print("Started application.")
    return app
