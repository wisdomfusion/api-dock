from flask import jsonify, request, g, current_app, url_for
from . import api
from ..models import User, Permission
from .errors import forbidden


@api.route('/users/')
def get_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.pagination(
        page,
        per_page=current_app.config.get('USER_PER_PAGE'),
        error_out=False
    )
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1)
    return jsonify({
        'users': [],
        'prev': prev,
        'next': next,
        'total': pagination.total
    })


@api.route('/users/<int:id>', methods=['GET', 'POST', 'PATCH'])
def get_user(id):
    # user = User.
    return ''
