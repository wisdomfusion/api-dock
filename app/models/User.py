import jwt
from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, validate
from . import db, ma
from .Permission import Permission
from .Role import Role


class User(db.Model):
    """This class represents the user table."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    status = db.Column(db.Integer, default=1)  # status: 1 normal, 2 blocked
    last_login_at = db.Column(db.DateTime, default=None)
    last_login_ip = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.name == current_app.config.get('APP_ROOT_ADMIN'):
                self.role = Role.query.filter_by(title='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def insert_root_admin():
        user = User(name='sysop',
                    password_hash=generate_password_hash('Passw0rd!'),
                    role_id=Role.query.filter_by(title='Administrator').first())

        db.session.add(user)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'last_login_at': self.last_login_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_ip': self.last_login_ip
        }

    def encode_auth_token(self):
        access_token = create_access_token(
            identity={'id': self.id, 'name': self.name},
            fresh=True,
            expires_delta=timedelta(minutes=int(current_app.config.get('JWT_TTL', 60)))
        )
        return access_token

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('JWT_SECRET'))
            print(payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please login again.'

    def __repr__(self):
        return '<User id:{} name:{}>'.format(self.id, self.name)


class UserSchema(ma.ModelSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3, 20))
    password = fields.String()
    role_id = fields.Integer()
    status = fields.Integer()
