import unittest
import datetime
from visbeer.services.beer_service import BeerService
from visbeer.services.coffee_service import CoffeeService
from visbeer.services.data_service import DataService, DATETIME_FORMAT
from visbeer.test.mocks.flag_service_mock import FlagServiceMock


class CoffeeBeerServiceTestCase(unittest.TestCase):

    def test_dispense_coffee(self):
        mock = FlagServiceMock()
        bs = BeerService('010101@rfid.ethz.ch', DataService(mock))
        cs = CoffeeService('010101@rfid.ethz.ch', DataService(mock))

        self.assertEqual(1, bs.status())
        self.assertEqual(2, cs.status())
        cs.dispensed()
        self.assertEqual(0, bs.status())
        self.assertEqual(1, cs.status())
        cs.dispensed()
        self.assertEqual(0, bs.status())
        cs.dispensed()
        self.assertEqual(0, bs.status())

        mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'] = 4
        self.assertEqual(2, bs.status())
        self.assertEqual(4, cs.status())
        cs.dispensed()
        self.assertEqual(3, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(1, bs.status())
        self.assertEqual(3, cs.status())
        cs.dispensed()
        self.assertEqual(2, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(1, bs.status())
        self.assertEqual(2, cs.status())
        cs.dispensed()
        self.assertEqual(1, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(1, cs.status())
        cs.dispensed()
        self.assertEqual(0, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())
        cs.dispensed()
        self.assertEqual(0, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())

    def test_dispense_beer(self):
        mock = FlagServiceMock()
        bs = BeerService('010101@rfid.ethz.ch', DataService(mock))
        cs = CoffeeService('010101@rfid.ethz.ch', DataService(mock))

        self.assertEqual(1, bs.status())
        self.assertEqual(2, cs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())

        mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'] = 4
        self.assertEqual(2, bs.status())
        self.assertEqual(4, cs.status())
        bs.dispensed()
        self.assertEqual(2, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(1, bs.status())
        self.assertEqual(2, cs.status())
        bs.dispensed()
        self.assertEqual(0, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())
        bs.dispensed()
        self.assertEqual(0, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())

    def test_dispense_mixed(self):
        mock = FlagServiceMock()
        bs = BeerService('010101@rfid.ethz.ch', DataService(mock))
        cs = CoffeeService('010101@rfid.ethz.ch', DataService(mock))

        self.assertEqual(1, bs.status())
        self.assertEqual(2, cs.status())
        bs.dispensed()
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())

        mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'] = 4
        self.assertEqual(2, bs.status())
        self.assertEqual(4, cs.status())
        cs.dispensed()
        self.assertEqual(3, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(1, bs.status())
        self.assertEqual(3, cs.status())
        bs.dispensed()
        self.assertEqual(1, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(1, cs.status())
        cs.dispensed()
        self.assertEqual(0, mock.data['010101@rfid.ethz.ch']['coffee_beer|credits'])
        self.assertEqual(0, bs.status())
        self.assertEqual(0, cs.status())


if __name__ == '__main__':
    unittest.main()
