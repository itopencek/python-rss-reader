from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/get/articles/<name>', methods=['GET'])
def get_articles(name):
    """
    Returns articles for given <site>.
    Site must be already in database.
    :param name: site name to get articles from
    :return:
    """
    # site = sites_dao.get_by_column('name', name)
    # html = WebReader().read(site['url'][0])
    # parsed = RssParser().parse(html)
    # return jsonify(parsed), 200


@api.route('/add/site/<name>', methods=['POST'])
def post_site(name):
    """
    Adds site to database.
    Must be valid.
    :param name: name of the site
    :return:
    """
    # body = request.get_json()
    # website = body['website']
    # if website == "":
    #     raise WrongParamException('website')
    # sites_dao = SitesDao()
    # site = sites_dao.get_object()
    # site['url'] = website
    # site['name'] = name
    # desc = body['desc']
    # if desc != "":
    #     site['desc'] = desc
    #
    # sites_dao.insert(site)
    # return return_status(200)


def return_status(status):
    return jsonify(status=status), 200
