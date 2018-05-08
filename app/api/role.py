from flask_restful import Resource
from app.api import api
from app.models.Role import Role, RoleSchema
from app.utils.response_helper import success

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


@api.resources('/roles')
class RoleList(Resource):
    """
    Role list
    """
    def get(self):
        roles = Role.query.all()
        result = roles_schema.dump(roles).data
        return success(result)
