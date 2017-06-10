import os
import flask
from ipdb import set_trace as DBG


# BUNDLE_ERRORS = True  #  flask-restful, for development only

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    API_BASE_URL = '/chessleague/'
    USE_RATE_LIMITS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL',
                                        'sqlite:///' + os.path.join(BASEDIR, 'chessleague_dev.db'))


class TestConfig(Config):
    SECRET_KEY = 'secret'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
                                        'sqlite:///' + os.path.join(BASEDIR, 'chessleague_test.db'))


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('CHESSLEAGUE_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'sqlite:///' + os.path.join(BASEDIR, 'chessleague.db'))


env = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name):
    conf = flask.Config(BASEDIR)
    conf.from_object(env[config_name])
    conf.from_pyfile('config.cfg', silent=True)
    return conf
