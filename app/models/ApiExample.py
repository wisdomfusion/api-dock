from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class ApiExample(db.Model):
    """Table to store APIs' examples, api_examples table."""
    __tablename__ = 'api_examples'

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return '<ApiExample {}>'.format(self.title)
