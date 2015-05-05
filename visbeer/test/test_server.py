import unittest
import os

from visbeer.server import app
from visbeer.test.mocks.beer_service_mock import BeerServiceMock


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['BeerService'] = BeerServiceMock
        app.config['ApiKey'] = 'llxPd3Krm2y4dLMa5YGCkLumvx0Mb1DZaZiPH'

    def authorized_get(self, url):
        return self.app.get(url + '?key=' + app.config['ApiKey'])

    def test_home(self):
        rv = self.app.get('/')
        self.assertEqual('api online', rv.data.decode('utf-8'))

    def test_validate_key(self):
        rv = self.app.get('/validate_key')
        self.assertEqual(401, rv.status_code)
        self.assertNotEqual('API key is valid', rv.data.decode('utf-8'))

        rv = self.app.get('/validate_key?key=' + 'some_invalid_key')
        self.assertEqual(401, rv.status_code)

        rv = self.app.get('/validate_key?key=' + app.config['ApiKey'])
        self.assertEqual('API key is valid', rv.data.decode('utf-8'))

    def test_status(self):
        self.assertEqual(401, self.app.get('/beer/status/010101@rfid.ethz.ch').status_code)

        self.assertEqual('1', self.authorized_get('/beer/status/010101@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('010101@rfid.ethz.ch', BeerServiceMock.lastRfidCallStatus)
        self.assertEqual('2', self.authorized_get('/beer/status/020202@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('020202@rfid.ethz.ch', BeerServiceMock.lastRfidCallStatus)

    def test_dispensed(self):
        self.assertEqual(401, self.app.get('/beer/dispensed/010101@rfid.ethz.ch').status_code)

        self.assertEqual('77', self.authorized_get('/beer/dispensed/010101@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('010101@rfid.ethz.ch', BeerServiceMock.lastRfidCallDispensed)
        self.assertEqual('77', self.authorized_get('/beer/dispensed/020202@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('020202@rfid.ethz.ch', BeerServiceMock.lastRfidCallDispensed)


if __name__ == '__main__':
    unittest.main()
