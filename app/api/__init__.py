from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix='/api/v1')

from . import auth, users, logs, apis, apps, api_groups, api_responses, api_examples
