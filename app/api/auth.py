from flask import request, make_response, jsonify
from flask_restful import Resource
from app.api import api
from app.models.User import User


@api.resource('/login')
class UserLogin(Resource):
    def post(self):
        data = request.get_json(force=True)
        if not data:
            response = {
                'status': 'error',
                'message': 'Invalid data.'
            }
            return make_response(jsonify(response), 400)

        try:
            user = User.query.filter_by(
                name=data.get('name')
            ).first()
            if user and user.verify_password(data.get('password')):
                token = user.encode_auth_token().decode('utf-8')
                if token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'token': token
                    }
                    return make_response(jsonify(response), 200, {'Authorization': 'Bearer: ' + token})
            else:
                response = {
                    'status': 'error',
                    'message': 'User do not exist.'
                }
                return make_response(jsonify(response), 404)
        except Exception as e:
            response = {
                'status': 'error',
                'message': 'Please try again.'
            }
            return make_response(jsonify(response), 500)


@api.resource('/logout')
class UserLogout(Resource):
    def post(self):
        return {'message': 'User Logout'}
