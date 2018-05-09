from flask import request, current_app, url_for
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.api import api
from app.models.User import User, UserSchema
from app.utils.response_helper import (
    success,
    error,
    not_found,
    unprocessable_entity,
    internal_error
)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.resource('/users', endpoint='api_users')
class UsersList(Resource):
    """
    Users list and new user
    """
    @jwt_required
    def get(self, page=1):
        data = request.get_json()

        if data and data.get('page'):
            page = data.get('page')
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

        return success(response_data)

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return error(message='Invalid data.')

        data, errors = user_schema.load(json_data)
        if errors:
            return unprocessable_entity(data=errors)

        user = User.query.filter_by(name=data.get('name')).first()
        if user:
            return error(
                message='User `{}` already exists.'.format(data.get('name'))
            )

        user = User(**data)
        try:
            user.save()
            result = user_schema.dump(user).data
            return success(result, 'Successfully add new user.')
        except Exception as e:
            return internal_error()


@api.resource('/users/<int:id>')
class UserItem(Resource):
    """
    Show user, edit user, and delete user
    """
    @jwt_required
    def get(self, id):
        user = User.query.get(id)

        if not user:
            return not_found('User does not exists.')

        result = user_schema.dump(user).data

        return success(result)

    @jwt_required
    def patch(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
            return error(message='Invalid data.')

        data, errors = user_schema.load(json_data)
        if errors:
            return unprocessable_entity(data=errors)

        user = User.query.get(id)
        if not user:
            return not_found('User does not exists.')

        if data.get('password'):
            user.password = data.get('password')
        user.role_id = data.get('role_id')
        user.status = data.get('status')
        user.updated_at = datetime.utcnow()

        try:
            user.save()
            result = user_schema.dump(user).data
            return success(result, 'Successfully edit a user.')
        except Exception as e:
            return internal_error()

    @jwt_required
    def delete(self, id):
        user = User.query.get(id)

        if not user:
            return not_found('User does not exists.')

        user.deleted_at = datetime.utcnow()

        try:
            user.save()
            result = user_schema.dump(user).data
            return success(result, 'Successfully delete a user.')
        except Exception as e:
            return internal_error()
