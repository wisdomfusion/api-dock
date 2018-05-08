from flask import jsonify, make_response
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = {'error': 'bad request', 'message': message}
    return make_response(jsonify(response), 400)


def unauthorized(message):
    response = {'error': 'unauthorized', 'message': message}
    return make_response(jsonify(response), 401)


def forbidden(message):
    response = {'error': 'forbidden', 'message': message}
    return make_response(jsonify(response), 403)


# @api.errorhandler(ValidationError)
# def validation_error(e):
#     return bad_request(e.args[0])
