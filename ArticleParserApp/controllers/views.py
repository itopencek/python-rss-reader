from flask import Blueprint, render_template

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
