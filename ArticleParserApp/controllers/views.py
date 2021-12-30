from flask import Blueprint, render_template, request

from ArticleParserApp.services.site import get_all_sites
from ArticleParserApp.services.stats import get_most_recent_articles, get_most_used_words, num_of_articles_by_sites, \
    get_num_of_articles

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def get_home():
    """
    Renders home page.
    :return: rendered home page
    """
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        # user probably typed string instead of int
        page = 1

    if page < 1:
        page = 1

    # we are showing 5 articles per page
    limit = 5
    max_articles = get_num_of_articles()

    # we need page - 1, because we want indexing for pages to be readable by humans (starting at 1 not 0)
    # if we want to show more than max articles
    if ((page - 1) * limit) + 1 > max_articles:
        page = 1

    articles = get_most_recent_articles(limit, ((page - 1) * limit))
    return render_template('index.html', articles=articles, data={'max': max_articles, 'limit': limit,
                                                                  'page': page})


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


@views.route('/stats', methods=['GET'])
def get_stats():
    """
    Renders stats page.
    :return: rendered stats page
    """
    most_used_words = get_most_used_words()
    num_of_articles = num_of_articles_by_sites()
    return render_template('stats.html', words=most_used_words, articles=num_of_articles)
