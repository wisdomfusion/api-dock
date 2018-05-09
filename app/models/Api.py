from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class Api(db.Model):
    """This class represents apis table."""
    __tablename__ = 'apis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('api_groups.id'))
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    request_url = db.Column(db.String(256), nullable=False)
    request_method = db.Column(db.String(10), nullable=False, default='GET')
    request_header = db.Column(db.Text, nullable=True)
    need_auth = db.Column(db.Boolean, default=0)    # 0 No auth required, 1 auth required
    status = db.Column(db.SmallInteger, default=1)  # 1, 2, 3
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)
    api_responses = db.relationship('ApiResponse', backref='api', lazy='dynamic')
    api_examples = db.relationship('ApiExample', backref='api', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Api, self).__init__(**kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Api {}>'.format(self.title)
