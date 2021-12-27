from flask import Blueprint, jsonify, request

from ArticleParserApp.database.models.exceptions.api import WrongParamException
from ArticleParserApp.database.models.models import Site
from ArticleParserApp.services.article import save_articles_from_site, get_articles_from_site
from ArticleParserApp.services.site import get_site_from_name, add_site, remove_site_by_id

api = Blueprint('api', __name__)


@api.route('/articles/<name>', methods=['GET'])
def get_articles(name):
    """
    Returns articles for given site name.
    Site must be already in database. Otherwise, WrongParamException is raised.
    :param name: site name to get articles from
    :return: articles with status 200
    """
    articles = get_articles_from_site(name)

    return jsonify(articles), 200


@api.route('/articles/<name>', methods=['PUT'])
def save_articles(name):
    """
    Saves articles from site to database.
    :param name: site name to use
    :return: site with status 200
    """
    site = Site.query.filter_by(name=name).first()
    if site is None:
        raise WrongParamException('name')

    if save_articles_from_site(site):
        return jsonify(site.as_dict()), 200
    else:
        return 500


@api.route('/site/<name>', methods=['GET'])
def get_site(name):
    """
    Gets site from its name. Site must be in database. If no name is found throws WrongParamException.
    :param name: name of site
    :return: site with status 200
    """
    site = get_site_from_name(name)

    return jsonify(site.as_dict()), 200


@api.route('/site', methods=['POST'])
def post_site():
    """
    Adds site to database.
    Must be valid.
    :return:
    """
    body = request.get_json()

    if not body or body == "":
        raise WrongParamException('site')

    add_site(body)

    return return_status(200)


@api.route('/site/delete/<site_id>', methods=['POST'])
def delete_site(site_id):
    """
    Removes site from database.
    Must be valid.
    NOTE: HTML5 forms do NOT support DELETE and PUT methods.
    https://stackoverflow.com/a/4052011
    :param site_id: id of site
    """
    if not site_id or site_id == "":
        raise WrongParamException('site_id')

    remove_site_by_id(site_id)

    return return_status(200)


# TODO check the return statement
def return_status(status):
    """
    Returns status in JSON format.
    """
    return jsonify(status=status), status
