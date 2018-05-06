from flask import request, g, jsonify
from flask_restful import Resource
from . import api
from ..models import User


@api.resource('/login')
class Login(Resource):
    def post(self):
        return {}, 200
