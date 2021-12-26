from ArticleParserApp import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    articles = db.relationship('Article', backref='site', lazy=True)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    @staticmethod
    def from_parsed(article, site_id):
        return Article(url=article['url'], name=article['title'], description=article['description'],
                       image_url=None, date=article['published'], site_id=site_id)
