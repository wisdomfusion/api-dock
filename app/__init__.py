from flask import Flask
from flask_cors import CORS
from config import config
from app.models import db


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config[config_name].init_app(app)

    db.init_app(app)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint)

    @app.route('/')
    def index():
        return 'API Dock, a web application for managing and testing your APIs.'

    return app
