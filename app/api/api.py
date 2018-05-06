from flask import jsonify, request, g, current_app, url_for
from flask_restful import Resource
from app.api import api
from app.models.Api import Api


@api.resource('/apis')
class APIList(Resource):
    def get(self):
        apis = Api.query.all()
        return jsonify(apis)

    def post(self):
        return {}, 200


@api.resource('/apis/<int:id>')
class APIItem(Resource):
    def get(self, id):
        return id

    def put(self, id):
        return {}, 200

    def delete(self):
        return {}, 200


@api.resource('/apis/<int:id>/status')
class APIStatus(Resource):
    def patch(self, id):
        return {}, 200
