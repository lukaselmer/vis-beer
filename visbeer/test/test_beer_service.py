import unittest
import datetime

from visbeer.services.beer_service import BeerService
from visbeer.services.beer_service import DATETIME_FORMAT
from visbeer.services.data_service import DataService
from visbeer.test.mocks.flag_service_mock import FlagServiceMock


class BeerServiceTestCase(unittest.TestCase):
    def test_ctor(self):
        self.assertEqual('010101@rfid.ethz.ch', BeerService('010101@rfid.ethz.ch', DataService(FlagServiceMock())).rfid)
        self.assertEqual('010203@rfid.ethz.ch', BeerService('010203@rfid.ethz.ch', DataService(FlagServiceMock())).rfid)

    def test_invalid_rfid(self):
        with self.assertRaises(Exception):
            BeerService('12345@rfid.ethz.ch', None)
        with self.assertRaises(Exception):
            BeerService('1234567@rfid.ethz.ch', None)
        with self.assertRaises(Exception):
            BeerService('@rfid.ethz.ch', None)
        with self.assertRaises(Exception):
            BeerService('rfid.ethz.ch', None)
        with self.assertRaises(Exception):
            BeerService('awefefw@rfid.ethz.ch', None)
        with self.assertRaises(Exception):
            BeerService('awefefw@', None)
        with self.assertRaises(Exception):
            BeerService('awefefw@whatever.com', None)
        with self.assertRaises(Exception):
            BeerService('234234', None)
        with self.assertRaises(Exception):
            BeerService('234@2q3r', None)

    def test_status(self):
        mock = FlagServiceMock()
        bs = BeerService('010101@rfid.ethz.ch', DataService(mock))

        self.assertEqual(1, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 10
        self.assertEqual(10, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = None
        self.assertEqual(10, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 5
        three_years_ago = (datetime.datetime.now() - datetime.timedelta(days=3 * 365)).strftime(DATETIME_FORMAT)
        mock.data['010101@rfid.ethz.ch']['beer|last'] = three_years_ago
        self.assertEqual(10, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 5
        one_day_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(DATETIME_FORMAT)
        mock.data['010101@rfid.ethz.ch']['beer|last'] = one_day_ago
        self.assertEqual(10, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 5
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(5, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 2
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(2, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 1
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(1, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 1
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 1
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(1, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 1
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 0
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(0, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|perday'] = 10
        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 0
        mock.data['010101@rfid.ethz.ch']['beer|last'] = datetime.datetime.now().strftime(DATETIME_FORMAT)
        self.assertEqual(0, bs.status())

    def test_status_and_dispensed(self):
        mock = FlagServiceMock()
        bs = BeerService('010101@rfid.ethz.ch', DataService(mock))

        self.assertEqual(1, bs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())

        mock.data['010101@rfid.ethz.ch']['beer|remaining'] = 2
        self.assertEqual(2, bs.status())
        bs.dispensed()
        self.assertEqual(1, bs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())


if __name__ == '__main__':
    unittest.main()
