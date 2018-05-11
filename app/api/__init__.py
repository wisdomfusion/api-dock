from flask import Blueprint, g
from flask_restful import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix='/api/v1')

from . import auth, user, app, api, api_group, api_response, api_example
