from flask import current_app, request, url_for
from marshmallow import fields, validate
from . import db, ma
from .Permission import Permission


class Role(db.Model):
    """This class represents the role table."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [
                # TODO
            ],
            'Developer': [
                Permission.LIST_USERS
            ],
            'QA': [
                Permission.LIST_USERS,
                Permission.ADD_USER,
                Permission.Edit_USER,
                Permission.BLOCK_USER
            ],
            'Administrator': [
                Permission.ADMIN,

                Permission.LIST_USERS,
                Permission.ADD_USER,
                Permission.Edit_USER,
                Permission.DELETE_USER,
                Permission.BLOCK_USER,

            ]
        }

        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(title=r).first()
            if role is None:
                role = Role(title=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.title == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role {}>'.format(self.title)


class RoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(2, 80))
    default = fields.Boolean()
