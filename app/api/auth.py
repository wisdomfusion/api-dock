from flask import request, g, jsonify
from flask_restful import Resource
from app.api import api
from app.models.User import User


@api.resource('/login')
class UserLogin(Resource):
    def post(self):
        return {'message': 'User Login'}


@api.resource('/logout')
class UserLogout(Resource):
    def post(self):
        return {'message': 'User Logout'}
