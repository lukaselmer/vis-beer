import unittest
from visbeer.services.beer_service import BeerService


class ServerTestCase(unittest.TestCase):
    def test_ctor(self):
        self.assertEqual('010101@rfid.ethz.ch', BeerService('010101@rfid.ethz.ch').rfid)
        self.assertEqual('010203@rfid.ethz.ch', BeerService('010203@rfid.ethz.ch').rfid)

    def test_invalid_rfid(self):
        with self.assertRaises(Exception):
            BeerService('12345@rfid.ethz.ch')
        with self.assertRaises(Exception):
            BeerService('1234567@rfid.ethz.ch')
        with self.assertRaises(Exception):
            BeerService('@rfid.ethz.ch')
        with self.assertRaises(Exception):
            BeerService('rfid.ethz.ch')
        with self.assertRaises(Exception):
            BeerService('awefefw@rfid.ethz.ch')
        with self.assertRaises(Exception):
            BeerService('awefefw@')
        with self.assertRaises(Exception):
            BeerService('awefefw@whatever.com')
        with self.assertRaises(Exception):
            BeerService('234234')
        with self.assertRaises(Exception):
            BeerService('234@2q3r')


if __name__ == '__main__':
    unittest.main()
