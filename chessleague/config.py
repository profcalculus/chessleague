import os
from ipdb import set_trace as DBG


# BUNDLE_ERRORS = True  #  flask-restful, for development only

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BASE_URL = '/chessleague'
    USE_RATE_LIMITS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'chessleague_dev.db')

class TestConfig(object):
    SECRET_KEY = 'secret'
    TESTING=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://' + os.path.join(BASEDIR, 'chessleague_test.db')

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite://' + os.path.join(BASEDIR, 'chessleague.db')

env = {
        'development': DevelopmentConfig,
        'testing': TestConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }

def configure_app(app, config_name=None):
    config_name = config_name or os.getenv('CHESSLEAGUE_CONFIG', 'default')
    app.config.from_object(env[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
