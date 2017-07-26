# chessleague/test/__init__.py

import unittest

from .test_client import TestClient
from .. import create_app

class ApiTest(unittest.TestCase):
    default_username = 'fred'
    default_password = 'bloggs'

    def setUp(self):
        try:
            self.app = create_app('testing')
            self.addCleanup(self.cleanUp)
            self.ctx = self.app.app_context()
            self.ctx.push()
            # from ..models import db
            # self.db = db
            # self.db.session.commit()
            # self.db.drop_all(app=self.app)
            from ..models import User, Player, Team, Match, Game, db
            self.db=db
            # self.app.logger.debug('drop_all())')
            self.db.create_all(app=self.app)
            # self.app.logger.debug('create_all())')
            user = User(user_name=self.default_username)
            user.password = self.default_password
            self.db.session.add(user)
            self.db.session.commit()
            self.client = TestClient(self.app, user.generate_auth_token(), '')
        except Exception, ex:
            self.app.logger.error("Error during setUp: %s" % ex)
            raise

    def cleanUp(self):
        try:
            self.db.session.commit()
            self.db.session.remove()
            self.db.drop_all(app=self.app)
            # self.app.logger.debug('drop_all())')
            self.ctx.pop()
        except Exception, ex:
            self.app.logger.error("Error during cleanUp: %s" % ex)
            raise
