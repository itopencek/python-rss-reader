from flask import Blueprint, jsonify

from src.models.exceptions.api import APIexception

exception = Blueprint('exception', __name__)


@exception.app_errorhandler(APIexception)
def api_exception_handler(wrong_param):
    error_obj = jsonify(message='Wrong or missing parameter', status=400, parameter=str(wrong_param))
    return error_obj, 400
