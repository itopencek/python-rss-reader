from flask import Blueprint, request, jsonify

from src.database.sitesdao import SitesDao
from src.models.exceptions.api import WrongParamException

api = Blueprint('api', __name__)


@api.route('/get/articles/<site>', methods=['GET'])
def get_articles(site):
    """
    Returns articles for given <site>.
    Site must be already in database.
    :param site: site name to get articles from
    :return:
    """


@api.route('/add/site/<name>', methods=['POST'])
def post_site(name):
    """
    Adds site to database.
    Must be valid.
    :param name: name of the site
    :return:
    """
    body = request.get_json()
    website = body['website']
    if website == "":
        raise WrongParamException('website')
    sites_dao = SitesDao()
    site = sites_dao.get_object()
    site['url'] = website
    site['name'] = name
    desc = body['desc']
    if desc != "":
        site['desc'] = desc

    sites_dao.insert(site)
    return return_status(200)


def return_status(status):
    return jsonify(status=status), 200
