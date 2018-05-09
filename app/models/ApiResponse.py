from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class ApiResponse(db.Model):
    """This class represents api_responses table, which holds APIs' responses."""
    __tablename__ = 'api_responses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'))
    field = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    nullable = db.Column(db.Boolean, default=True)
    data_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def __init__(self, **kwargs):
        super(ApiResponse, self).__init__(**kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<ApiResponse {}>'.format(self.key)
