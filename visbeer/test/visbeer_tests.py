import os
import visbeer.server
import unittest
import tempfile


class VisbeerTestCase(unittest.TestCase):
    def setUp(self):
        # self.db_fd, visbeer.app.config['DATABASE'] = tempfile.mkstemp()
        #visbeer.app.config['TESTING'] = True
        self.app = visbeer.server.app.test_client()
        #visbeer.init_db()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        #os.unlink(visbeer.app.config['DATABASE'])

    def test_home(self):
        rv = self.app.get('/')
        print(rv.data)
        assert 'Hello, World!' in rv.data.decode('utf-8')


if __name__ == '__main__':
    unittest.main()
