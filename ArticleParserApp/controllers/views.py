from flask import Blueprint, render_template

from ArticleParserApp.services.site import get_all_sites
from ArticleParserApp.services.stats import get_most_recent_articles

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def get_home():
    """
    Renders home page.
    :return: rendered home page
    """
    articles = get_most_recent_articles(5)
    return render_template('index.html', articles=articles)


@views.route('/sites', methods=['GET'])
def get_sites():
    """
    Renders sites page.
    :return: rendered site page
    """
    sites = get_all_sites()
    return render_template('sites.html', sites=sites)


@views.route('/add-site', methods=['GET'])
def get_add_site():
    """
    Renders add-site page.
    :return: rendered add-site page
    """
    return render_template('add-site.html')
