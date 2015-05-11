import datetime
from visbeer.services.service_helper import beginning_of_current_day, DEFAULT_CREDITS_PER_DAY

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DataService:
    def __init__(self, flag_service):
        self.flag_service = flag_service

    def find_person(self, rfid):
        return self.flag_service.find_person(rfid)

    def is_developer(self, person):
        val = self.flag_service.get_flag_value('coffee_beer', person, 'developer')
        return val and len(val) >= 1

    def _get_last(self, person):
        raw = self.flag_service.get_flag_value('coffee_beer', person, 'last_consumption')

        if not raw:
            return None

        return datetime.datetime.strptime(raw, DATETIME_FORMAT)

    def set_last(self, person, last_time):
        raw = last_time.strftime(DATETIME_FORMAT)
        self.flag_service.set_flag_value('coffee_beer', person, 'last_consumption', raw)

    def _get_credits_per_day(self, person):
        return int(self.flag_service.get_flag_value('coffee_beer', person, 'credits_per_day'))

    def _set_default_credits_per_day(self, person, default):
        self.flag_service.set_default_flag_value('coffee_beer', person, 'credits_per_day', int(default))

    def _get_credits(self, person):
        return int(self.flag_service.get_flag_value('coffee_beer', person, 'credits'))

    def set_credits(self, person, amount):
        self.flag_service.set_flag_value('coffee_beer', person, 'credits', int(amount))

    def has_consumed_today(self, person):
        last_consumption = self._get_last(person)

        if not last_consumption:
            # this is the case if someone never consumed a beverage until now
            return False

        return last_consumption >= beginning_of_current_day()

    def credits_per_day(self, person):
        self._set_default_credits_per_day(person, DEFAULT_CREDITS_PER_DAY)
        return self._get_credits_per_day(person)

    def remaining_credits(self, person):
        return self._get_credits(person)
