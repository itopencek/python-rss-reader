from ArticleParserApp.controllers.exceptions import exception
from ArticleParserApp.parser.parser import RssParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import pandas as pd

app = Flask(__name__)
db = SQLAlchemy()
DB_PATH = 'sqlite:///database/database.db'
DB_NAME = 'database.db'
df_articles = None
df_sites = None


def register_blueprints():
    """
    Registers controllers.
    """
    from ArticleParserApp.controllers.views import views
    from ArticleParserApp.controllers.api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')


def register_exceptions():
    """
    Registers exception handler.
    """
    app.register_blueprint(exception)


def create_database():
    """
    Creates and set-ups database and Pandas DataFrame.
    """
    global df_articles, df_sites
    db.init_app(app)
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database.')
    else:
        print('Database already exists.')
    # set up pandas df
    with app.app_context():
        df_articles = pd.read_sql('SELECT * FROM article', con=db.engine)
        df_sites = pd.read_sql('SELECT * FROM site', con=db.engine)
    print("Set up pandas DataFrame.")


def set_config():
    """
    Sets basic configuration for app.
    """
    app.config['SECRET_KEY'] = 'very secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def main(test_config=None):
    from ArticleParserApp.database.models.models import Site, Article
    if test_config is None:
        set_config()
        create_database()
    else:
        app.config.from_mapping(test_config)

    register_exceptions()
    register_blueprints()
    print("Started application.")
    return app
