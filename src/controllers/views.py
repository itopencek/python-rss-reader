from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def get_home():
    """
    Renders home page.
    :return: home page
    """
    return '<h1>Test</h1>'
