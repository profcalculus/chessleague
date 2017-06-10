import os
import unittest
import tempfile
import json

import chessleague
from chessleague import api

from ipdb import set_trace as DBG


class APITest(unittest.TestCase):
    def setUp(self):
        self.db_fd, chessleague.app.config['DATABASE'] = tempfile.mkstemp()
        chessleague.app.config['TESTING'] = True
        self.app = chessleague.app.test_client()
        # with chessleague.app.app_context():
        #     chessleague.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(chessleague.app.config['DATABASE'])


class PlayerAPITest(APITest):
    def test_get_all(self):
        response = self.app.get(
            chessleague.app.config['API_BASE_URL'] + '/players')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data('players')), 10)


if __name__ == '__main__':
    unittest.main()
