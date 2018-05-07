from flask import request, make_response, jsonify, current_app
from datetime import datetime, timedelta
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from app.api import api
from app.models.User import User, UserSchema

user_schema = UserSchema()


@api.resource('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)

        if not json_data:
            return make_response({'status': 'error', 'message': 'Invalid data.'}, 400)

        data, errors = user_schema.load(json_data)

        if errors:
            return make_response(errors, 422)

        if not data:
            return make_response({'status': 'error', 'message': 'Invalid data.'}, 400)

        try:
            user = User.query.filter_by(name=data['name']).first()
            if user and user.verify_password(data['password']):
                access_token = user.encode_auth_token()
                if access_token:
                    response_data = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'access_token': access_token
                    }
                    return make_response(jsonify(response_data))
            else:
                response_data = {
                    'status': 'error',
                    'message': 'User do not exist.'
                }
                return make_response(jsonify(response_data), 404)
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': 'Internal Server Error'
            }
            return make_response(jsonify(response_data), 500)


@api.resource('/logout')
class UserLogout(Resource):
    """
    User Logout Resource
    """
    def post(self):
        return {'message': 'User Logout'}
