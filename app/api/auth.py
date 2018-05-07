from flask import request, make_response, jsonify
from flask_restful import Resource
from app.api import api
from app.models.User import User, UserSchema

user_schema = UserSchema


@api.resource('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    def post(self):
        json_data = request.get_json(force=True)

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
                token = user.encode_auth_token().decode('utf-8')
                if token:
                    response_data = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'token': token
                    }
                    return make_response(response_data, 200, {'Authorization': 'Bearer: ' + token})
            else:
                response_data = {
                    'status': 'error',
                    'message': 'User do not exist.'
                }
                return make_response(response_data, 404)
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': 'Internal Server Error'
            }
            return make_response(response_data, 500)


@api.resource('/logout')
class UserLogout(Resource):
    """
    User Logout Resource
    """
    def post(self):
        return {'message': 'User Logout'}


@api.resources('/refresh_token')
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'token refresh'}
