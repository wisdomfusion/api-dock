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
from . import api
from ..models.User import User
from ..models.RevokedToken import RevokedToken
from ..utils.response_helper import (
    success,
    error,
    not_found,
    unprocessable_entity,
    internal_error
)


@api.resource('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    def post(self):
        data = request.get_json(force=True)
        if not data:
            return error(message='Invalid data.')

        try:
            user = User.query.filter_by(name=data['name']).first()
            if not user:
                return not_found('User does not exists.')

            if user.verify_password(data['password']):
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
                return unprocessable_entity(data={
                    'mismatch': ["Mismatch between user's name or password"]
                })
        except Exception as e:
            return internal_error()


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
            return success(message='Access token has been revoked.')
        except Exception as e:
            return internal_error()


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
            return success(message='Access token has been revoked.')
        except Exception as e:
            return internal_error()


@api.resource('/token/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(minutes=int(current_app.config['JWT_TTL']))
        )
        return success({'access_token': access_token})
