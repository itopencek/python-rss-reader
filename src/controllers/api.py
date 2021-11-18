from flask import Blueprint, request

from src.models.exceptions.api import APIexception

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
    Must be valid.s
    :param name: name of the site
    :return:
    """
    website = request.args.get('website', default="", type="str")
    if website == "":
        raise APIexception('website')
