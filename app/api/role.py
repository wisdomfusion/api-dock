from flask import make_response
from flask_restful import Resource
from app.api import api
from app.models.Role import Role


@api.resources('/roles')
class RoleList(Resource):
    """
    Role list
    """
    def get(self):
        roles = Role.query.all()
        return make_response({'status': 'success', 'data': [role.to_json() for role in roles]})
