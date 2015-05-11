import re
import datetime
import math
from visbeer.services.data_service import DataService

ENABLE_BEER_CONSUMPTION = True
DEFAULT_CREDITS_PER_DAY = 2
RFID_REGEX = re.compile(r"[0-9]{6}@rfid\.ethz\.ch")


def beginning_of_current_day():
    cutoff = datetime.time(3, 0)
    if datetime.datetime.now().time() < cutoff:
        day = datetime.date.today() - datetime.timedelta(days=1)
    else:
        day = datetime.date.today()
    return datetime.datetime.combine(day, cutoff)


def validate_rfid(rfid):
    if not RFID_REGEX.match(rfid):
        raise Exception('Invalid rfid')


class BeerService:
    def __init__(self, rfid, data_service):
        validate_rfid(rfid)

        self.rfid = rfid
        self.data_service = data_service
        self.person = data_service.find_person(rfid)

    def status(self):
        if not ENABLE_BEER_CONSUMPTION and not self._is_developer():
            # enable API testing even if the beer consumption is disabled
            return 0

        if not self.person.vismember:
            # allow only vis members to drink beer
            return 0

        if not self._has_consumed_today():
            # no consumption today -> reset the remaining value
            self.data_service.set_credits(self.person, self._credits_per_day())

        return self._remaining_beers()

    def dispensed(self):
        remaining_beers = self.status()
        if remaining_beers <= 0:
            # Uh oh, something went wrong!?
            return 0

        self.data_service.set_last(self.person, datetime.datetime.now())
        self.data_service.set_credits(self.person, (remaining_beers - 1) * 2)

        return remaining_beers - 1

    def _has_consumed_today(self):
        last_consumption = self.data_service.get_last(self.person)

        if not last_consumption:
            # this is the case if someone never consumed a beverage until now
            return False

        return last_consumption >= beginning_of_current_day()

    def _remaining_beers(self):
        # for every 2 coffees, subtract on beer (at least)
        return int(math.floor(self._remaining_credits() / 2.0))

    def _is_developer(self):
        return self.data_service.is_developer(self.person)

    def _credits_per_day(self):
        self.data_service.set_default_credits_per_day(self.person, DEFAULT_CREDITS_PER_DAY)
        return self.data_service.get_credits_per_day(self.person)

    def _remaining_credits(self):
        return self.data_service.get_credits(self.person)
