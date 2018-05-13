import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    """Parent configuration class."""
    APP_CONFIG = os.getenv('APP_CONFIG', 'default')
    APP_URL = os.getenv('APP_URL')

    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    CACHE_DRIVER = os.getenv('CACHE_DRIVER')
    SESSION_DRIVER = os.getenv('SESSION_DRIVER')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_PORT = os.getenv('REDIS_PORT')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TTL = os.getenv('JWT_TTL', 60)

    APP_ROOT_ADMIN = os.getenv('APP_ROOT_ADMIN')

    USER_PER_PAGE = os.getenv('USER_PER_PAGE', 20)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, probably with a separate database."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_TEST_URI')


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DockerConfig(ProductionConfig):
    """Configurations for Docker environment."""
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}