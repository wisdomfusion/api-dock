from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from config import config

db = SQLAlchemy()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    moment.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    api = Api(app)

    return api
