from ArticleParserApp import db


class Site(db.Model):
    """
    Database model for site.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    language = db.Column(db.String, unique=False, nullable=False)
    articles = db.relationship('Article', backref='site', lazy=True)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Article(db.Model):
    """
    Database model for article.
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    # date is saved as EPOCH in String
    date = db.Column(db.String, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    def get_date(self):
        return self.date

    def set_date(self, new_date):
        self.date = new_date

    @staticmethod
    def from_parsed(article, site_id):
        """
        Creates Article from parsed article and site_id. Expects valid site_id.
        :param article: parsed article
        :param site_id: valid id of site
        :return: new Article object
        """
        return Article(url=article['url'], name=article['title'], description=article['description'],
                       image_url=None, date=article['published'], site_id=site_id)
