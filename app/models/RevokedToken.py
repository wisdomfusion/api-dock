from . import db


class RevokedToken(db.Model):
    """Token blacklist table."""
    ___tablename___ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(256))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        token = cls.query.filter_by(jti=jti).first()
        return bool(token)
