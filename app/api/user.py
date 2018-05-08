from flask import jsonify, request, make_response, g, current_app, url_for
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.api import api
from app.models.User import User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.resource('/users', endpoint='api_users')
class AllUsers(Resource):
    """
    User list and new user
    """
    @jwt_required
    def get(self, page=1):
        data = request.get_json()
        if data and data['page']:
            page = data['page']
        per_page = int(current_app.config.get('USER_PER_PAGE', 20))
        pagination = User.query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        users = users_schema.dump(pagination.items).data
        response_data = {
            'users': users,
            'page': pagination.page,
            'prev': url_for('api_users', page=page - 1) if pagination.has_prev else None,
            'next': url_for('api_users', page=page + 1) if pagination.has_next else None,
            'total': pagination.total
        }
        return make_response(jsonify(response_data))

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return make_response({'status': 'error', 'message': 'Invalid data.'}, 400)

        data, errors = user_schema.load(json_data)

        if errors:
            return make_response(errors, 422)

        user = User.query.filter_by(name=data['name']).first()

        if user:
            return make_response({'status': 'error', 'message': 'User `{}` already exists.'.format(data['name'])}, 400)

        user = User(**data)
        try:
            user.save()
            result = user_schema.dump(user).data
            response_data = {
                'status': 'success',
                'message': 'Successfully add new user.',
                'data': result
            }
            return make_response(response_data)
        except Exception as e:
            return make_response({'status': 'error', 'message': 'Internal Server Error'}, 500)


@api.resource('/users/<int:id>')
class UserItem(Resource):
    """
    Show user, edit user, and delete user
    """
    @jwt_required
    def get(id):
        user = User.query.get_or_404(id)
        response_data = {
            'status': 'success',
            'data': user_schema.dump(user).data
        }
        return make_response(response_data)

    @jwt_required
    def patch(id):
        json_data = request.get_json(force=True)

        if not json_data:
            return make_response({'status': 'error', 'message': 'Invalid data.'}, 400)

        data, errors = user_schema.load(json_data)

        if errors:
            return make_response(errors, 422)

        user = User.query.get_or_404(id)
        user.password(data['password'])
        user.role_id = data['role_id']
        user.status = data['status']
        user.updated_at = datetime.utcnow()

        try:
            user.save()
            response_data = {
                'status': 'success',
                'message': 'Successfully edit a user.',
                'data': user_schema.dump(user).data
            }
            return make_response(response_data)
        except Exception as e:
            return make_response({'status': 'error', 'message': 'Internal Server Error'}, 500)

    @jwt_required
    def delete(id):
        user = User.query.get_or_404(id)
        user.deleted_at = datetime.utcnow()

        try:
            user.save()
            response_data = {
                'status': 'success',
                'message': 'Successfully delete a user.',
                'data': user_schema.dump(user).data
            }
            return make_response(response_data)
        except Exception as e:
            return make_response({'status': 'error', 'message': 'Internal Server Error'}, 500)
