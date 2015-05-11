import datetime
import math
from visbeer.services.service_helper import validate_rfid, ENABLE_BEER_CONSUMPTION


class BeerService:
    def __init__(self, rfid, data_service):
        validate_rfid(rfid)

        self.rfid = rfid
        self.data_service = data_service
        self.person = data_service.find_person(rfid)

    def status(self):
        if not ENABLE_BEER_CONSUMPTION and not self.data_service.is_developer(self.person):
            # enable API testing even if the beer consumption is disabled
            return 0

        if not self.person.vismember:
            # allow only vis members to drink beer
            return 0

        if not self.data_service.has_consumed_today(self.person):
            # no consumption today -> reset the remaining value
            self.data_service.set_credits(self.person, self.data_service.credits_per_day(self.person))

        return self._remaining_beers()

    def dispensed(self):
        remaining_beers = self.status()
        if remaining_beers <= 0:
            # Uh oh, something went wrong!?
            return 0

        self.data_service.set_last(self.person, datetime.datetime.now())
        self.data_service.set_credits(self.person, (remaining_beers - 1) * 2)

        return remaining_beers - 1

    def _remaining_beers(self):
        # for every 2 coffees, subtract on beer (at least)
        return int(math.floor(self.data_service.remaining_credits(self.person) / 2.0))
