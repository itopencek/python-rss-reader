from ArticleParserApp import db
from ArticleParserApp.database.models.models import Article
from ArticleParserApp.parser.parser import RssParser
from ArticleParserApp.parser.reader import WebReader
from ArticleParserApp.services.site import get_site_from_name


def save_articles_from_site(name):
    """
    Saves all articles from site name. Site must be in database. Will skip articles, that are already in database.
    :param name: name of site to use
    """
    site = get_site_from_name(name)

    articles = parse_articles(site.url)
    for article in articles:
        if Article.query.filter_by(name=article['title']).first() or Article.query.filter_by(url=article['url']).first():
            print("Had to skip article with name \"" + article['title'] + "\", because it already exists!")
        else:
            new_article = Article().from_parsed(article, site.id)
            db.session.add(new_article)
    db.session.commit()
    return True


def get_articles_from_site(site):
    """
    Returns articles from site.
    :param site: site object
    :return: articles
    """
    return parse_articles(site.url)


def parse_articles(url):
    """
    Reads articles from given url. Must be url to RSS.
    :param url: url to RSS file
    :return: read and parsed articles
    """
    html = WebReader().read(url)
    return RssParser().parse(html)
