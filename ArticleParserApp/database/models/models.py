from ArticleParserApp import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    articles = db.relationship('Article', backref='site', lazy=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    site = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
