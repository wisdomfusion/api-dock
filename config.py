import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Parent configuration class."""
    APP_KEY = os.environ.get('APP_KEY')
    APP_URL = os.environ.get('APP_URL')

    DB_CONNECTION = os.environ.get('DB_CONNECTION')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('3306')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    CACHE_DRIVER = os.environ.get('CACHE_DRIVER')
    SESSION_DRIVER = os.environ.get('SESSION_DRIVER')

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_PORT = os.environ.get('REDIS_PORT')

    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_TTL = os.environ.get('JWT_TTL') or 60

    APP_ROOT_ADMIN = os.environ.get('APP_ROOT_ADMIN')

    USER_PER_PAGE = os.environ.get('USER_PER_PAGE') or 20

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