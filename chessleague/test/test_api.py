import os
import chessleague
import unittest
import tempfile

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, chessleague.app.config['DATABASE'] = tempfile.mkstemp()
        chessleague.app.config['TESTING'] = True
        self.app = chessleague.app.test_client()
        with chessleague.app.app_context():
            chessleague.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(chessleague.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
