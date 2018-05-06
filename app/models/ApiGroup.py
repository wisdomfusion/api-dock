from datetime import datetime, timedelta
from flask import current_app, request, url_for
from .shared import db


class ApiGroup(db.Model):
    """This class represents api_groups table."""
    __tablename__ = 'api_groups'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    title = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)
    api_list = db.relationship('Api', backref='api_group', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ApiGroup {}>'.format(self.title)