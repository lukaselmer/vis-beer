import os
from visbeer.server import app
import unittest
import tempfile


class BeerServiceMock:
    lastRfidCallStatus = ''
    lastRfidCallDispensed = ''

    def __init__(self, rfid):
        self.rfid = rfid

    def status(self):
        BeerServiceMock.lastRfidCallStatus = self.rfid
        if self.rfid == '010101@rfid.ethz.ch':
            return '1'
        elif self.rfid == '020202@rfid.ethz.ch':
            return '2'
        raise 'bad value'

    def dispensed(self):
        BeerServiceMock.lastRfidCallDispensed = self.rfid
        return '77'


class VisbeerServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['BeerService'] = BeerServiceMock

    def test_home(self):
        rv = self.app.get('/')
        self.assertEqual('api online', rv.data.decode('utf-8'))

    def test_status(self):
        self.assertEqual('1', self.app.get('/beer/status/010101@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('010101@rfid.ethz.ch', BeerServiceMock.lastRfidCallStatus)
        self.assertEqual('2', self.app.get('/beer/status/020202@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('020202@rfid.ethz.ch', BeerServiceMock.lastRfidCallStatus)

    def test_dispensed(self):
        self.assertEqual('77', self.app.get('/beer/dispensed/010101@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('010101@rfid.ethz.ch', BeerServiceMock.lastRfidCallDispensed)
        self.assertEqual('77', self.app.get('/beer/dispensed/020202@rfid.ethz.ch').data.decode('utf-8'))
        self.assertEqual('020202@rfid.ethz.ch', BeerServiceMock.lastRfidCallDispensed)


if __name__ == '__main__':
    unittest.main()
