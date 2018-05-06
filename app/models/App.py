from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class App(db.Model):
    """The class to manage apps table."""
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    version = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.SmallInteger, default=1)       # 1 Web, 2 APP, 3 PC, 4 other
    auth_type = db.Column(db.SmallInteger, default=0)  # 0 No Auth, 1 Basic Auth, 2 OAuth 2.0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)
    api_groups = db.relationship('ApiGroup', backref='app', lazy='dynamic')

    def __repr__(self):
        return '<App {}>'.format(self.title)
