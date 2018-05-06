from flask import jsonify, request, g, current_app, url_for
from flask_restful import Resource
from app.api import api
from app.models.App import App


@api.resource('/apps')
class AppList(Resource):
    def get(self):
        apps = App.query.all()
        return jsonify(apps)

    def post(self):
        return {}, 200


@api.resource('/apps/<int:id>')
class AppItem(Resource):
    def get(self, id):
        # app
        return id

    def put(self):
        return {}, 200

    def delete(self):
        return {}, 200
