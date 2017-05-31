import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chessleague.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

BUNDLE_ERRORS = True  #  flask-restful, for development only


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BASE_URL = '/chessleague'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'chessleague_dev.db')

class TestConfig(object):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/chessleague.db'
    TESTING=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'chessleague_test.db')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'chessleague.db')

Config.environment = {
        'development': DevelopmentConfig,
        'testing': TestConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
