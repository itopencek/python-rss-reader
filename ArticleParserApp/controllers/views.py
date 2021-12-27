from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def get_home():
    """
    Renders home page.
    :return: rendered home page
    """
    return render_template('index.html')
