from flask import Flask, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from app.models import db, ma
from app.models.RevokedToken import RevokedToken


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config[config_name].init_app(app)
    app.secret_key = app.config['APP_KEY']

    db.init_app(app)
    ma.init_app(app)

    jwt = JWTManager(app)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint)

    @app.route('/')
    def index():
        return 'API Dock, a web application for managing and testing your APIs.'

    return app
