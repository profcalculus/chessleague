import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chessleague.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

BUNDLE_ERRORS = True  #  flask-restful, for development only

BASE_URL = '/chessleague'

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/chessleague.db'
    testing=True
    debug=True
