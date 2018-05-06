from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class Log(db.Model):
    """This class create logs table, to record users' actions."""
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Log {}>'.format(self.action)
