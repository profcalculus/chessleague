import os
import flask
import logging


# BUNDLE_ERRORS = True  #  flask-restful, for development only

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_BASE_URL = '/api/1.0'
    USE_RATE_LIMITS = False
    USE_TOKEN_AUTH = True
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL', 'sqlite:///' + os.path.join(
            BASEDIR, 'chessleague_dev.db'))


class TestConfig(Config):
    SECRET_KEY = 'secret'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL', 'sqlite:///' + os.path.join(
            BASEDIR, 'chessleague_test.db'))


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('CHESSLEAGUE_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(
        BASEDIR, 'chessleague.db'))
    LOG_LEVEL = logging.INFO

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
