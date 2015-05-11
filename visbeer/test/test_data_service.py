import unittest
import datetime

from visbeer.services.beer_service import BeerService
from visbeer.services.beer_service import DATETIME_FORMAT
from visbeer.services.data_service import DataService
from visbeer.test.mocks.flag_service_mock import FlagServiceMock


class DataServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.mock = FlagServiceMock()
        self.rfid1 = '010101@rfid.ethz.ch'
        self.rfid2 = '010103@rfid.ethz.ch'
        self.person1 = self.mock.find_person(self.rfid1)
        self.person2 = self.mock.find_person(self.rfid2)
        self.ds = DataService(self.mock)

    def test_no_limit(self):
        self.assertEqual(None, self.ds.get_beer_no_limit(self.person1))
        self.mock.data[self.rfid1]['nolimit'] = 1
        self.assertEqual('1', self.ds.get_beer_no_limit(self.person1))

    def test_no_limit(self):
        self.assertEqual(None, self.ds.get_beer_dispensed_today(self.person1))
        self.mock.data[self.rfid1]['dispensed_today'] = 1
        self.assertEqual('1', self.ds.get_beer_dispensed_today(self.person1))

    def test_beer_per_day(self):
        self.assertEqual(None, self.ds.get_beer_per_day(self.person1))
        self.ds.set_default_beers_per_day(self.person1, 10)
        self.assertEqual('10', self.ds.get_beer_per_day(self.person1))
        self.ds.set_default_beers_per_day(self.person1, 20)
        self.assertEqual('10', self.ds.get_beer_per_day(self.person1))

    def test_beer_remaining(self):
        self.assertEqual(None, self.ds.get_beer_remaining(self.person1))
        self.ds.set_beer_remaining(self.person1, 10)
        self.assertEqual('10', self.ds.get_beer_remaining(self.person1))
        self.ds.set_beer_remaining(self.person1, 20)
        self.assertEqual('20', self.ds.get_beer_remaining(self.person1))

    def test_beer_last(self):
        self.assertEqual(None, self.ds.get_beer_last(self.person1))
        self.ds.set_beer_last(self.person1, 10)
        self.assertEqual('10', self.ds.get_beer_last(self.person1))
        self.ds.set_beer_last(self.person1, 20)
        self.assertEqual('20', self.ds.get_beer_last(self.person1))


if __name__ == '__main__':
    unittest.main()
