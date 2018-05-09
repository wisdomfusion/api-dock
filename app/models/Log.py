from datetime import datetime, timedelta
from flask import current_app, request, url_for
from . import db


class Log(db.Model):
    """This class create logs table, to record users' actions."""
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Log, self).__init__(**kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Log {}>'.format(self.action)
