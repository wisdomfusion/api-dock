from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class ApiExample(db.Model):
    """Table to store APIs' examples, api_examples table."""
    __tablename__ = 'api_examples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def __init__(self, **kwargs):
        super(ApiExample, self).__init__(**kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<ApiExample {}>'.format(self.title)
