from flask import request, make_response, jsonify, current_app
from datetime import timedelta
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
from app.models.User import User
from app.models.RevokedToken import RevokedToken


@api.resource('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    def post(self):
        data = request.get_json(force=True)
        if not data:
            return make_response({'status': 'error', 'message': 'Invalid data.'}, 400)

        try:
            user = User.query.filter_by(name=data['name']).first()

            if user and user.verify_password(data['password']):
                identity = {'id': user.id, 'name': user.name}
                access_token = create_access_token(
                    identity=identity,
                    expires_delta=timedelta(minutes=int(current_app.config['JWT_TTL']))
                )
                refresh_token = create_refresh_token(identity=identity)

                if access_token and refresh_token:
                    response_data = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'data': {
                            'user': identity,
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }
                    }
                    return make_response(jsonify(response_data))
            else:
                response_data = {
                    'status': 'error',
                    'message': 'User do not exist.'
                }
                return make_response(jsonify(response_data), 404)
        except Exception as e:
            return make_response(jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500)


@api.resource('/logout/access')
class LogoutAccess(Resource):
    """
    User Logout Resource
    """
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return make_response(jsonify({'status': 'success', 'message': 'Access token has been revoked'}))
        except Exception as e:
            return make_response(jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500)


@api.resource('/logout/refresh')
class LogoutRefresh(Resource):
    """
    User Logout Refresh
    """
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return make_response(jsonify({'status': 'success', 'message': 'Access token has been revoked'}))
        except Exception as e:
            return make_response(jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500)


@api.resource('/token/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(minutes=int(current_app.config['JWT_TTL']))
        )
        return access_token
