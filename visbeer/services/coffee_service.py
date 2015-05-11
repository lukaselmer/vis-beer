import datetime
from visbeer.services.service_helper import validate_rfid, ENABLE_COFFEE_CONSUMPTION


class CoffeeService:
    def __init__(self, rfid, data_service):
        validate_rfid(rfid)

        self.rfid = rfid
        self.data_service = data_service
        self.person = data_service.find_person(rfid)

    def status(self):
        if not ENABLE_COFFEE_CONSUMPTION and not self.data_service.is_developer(self.person):
            # enable API testing even if the coffee consumption is disabled
            return 0

        if not self.person.vismember:
            # allow only vis members to drink coffee
            return 0

        if not self.data_service.has_consumed_today(self.person):
            # no consumption today -> reset the remaining value
            self.data_service.set_credits(self.person, self.data_service.credits_per_day(self.person))

        return self._remaining_coffees()

    def dispensed(self):
        remaining_coffees = self.status()
        if remaining_coffees <= 0:
            # Uh oh, something went wrong!?
            return 0

        self.data_service.set_last(self.person, datetime.datetime.now())
        self.data_service.set_credits(self.person, remaining_coffees - 1)

        return remaining_coffees - 1

    def _remaining_coffees(self):
        # for every 2 coffees, subtract on coffee (at least)
        return self.data_service.remaining_credits(self.person)
