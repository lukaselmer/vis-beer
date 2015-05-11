import unittest
import datetime

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

    def test_is_developer(self):
        self.assertFalse(self.ds.is_developer(self.person1))
        self.mock.data[self.rfid1]['coffee_beer|developer'] = '1'
        self.assertTrue(self.ds.is_developer(self.person1))

    def test_beer_per_day(self):
        self.ds.set_default_credits_per_day(self.person1, 10)
        self.assertEqual(10, self.ds.get_credits_per_day(self.person1))
        self.ds.set_default_credits_per_day(self.person1, 20)
        self.assertEqual(10, self.ds.get_credits_per_day(self.person1))

    def test_beer_remaining(self):
        self.ds.set_credits(self.person1, 10)
        self.assertEqual(10, self.ds.get_credits(self.person1))
        self.ds.set_credits(self.person1, 20)
        self.assertEqual(20, self.ds.get_credits(self.person1))

    def test_beer_last(self):
        self.assertEqual(None, self.ds.get_last(self.person1))
        nearly_now = datetime.datetime.now().replace(microsecond=0)
        self.ds.set_last(self.person1, nearly_now)
        self.assertEqual(nearly_now, self.ds.get_last(self.person1))


if __name__ == '__main__':
    unittest.main()
