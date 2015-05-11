import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DataService:
    def __init__(self, flag_service):
        self.flag_service = flag_service

    def find_person(self, rfid):
        return self.flag_service.find_person(rfid)

    def is_developer(self, person):
        val = self.flag_service.get_flag_value('coffee_beer', person, 'developer')
        return val and len(val) >= 1

    def get_last(self, person):
        raw = self.flag_service.get_flag_value('coffee_beer', person, 'last_consumption')

        if not raw:
            return None

        return datetime.datetime.strptime(raw, DATETIME_FORMAT)

    def set_last(self, person, last_time):
        raw = last_time.strftime(DATETIME_FORMAT)
        self.flag_service.set_flag_value('coffee_beer', person, 'last_consumption', raw)

    def get_credits_per_day(self, person):
        return int(self.flag_service.get_flag_value('coffee_beer', person, 'credits_per_day'))

    def set_default_credits_per_day(self, person, default):
        self.flag_service.set_default_flag_value('coffee_beer', person, 'credits_per_day', int(default))

    def get_credits(self, person):
        return int(self.flag_service.get_flag_value('coffee_beer', person, 'credits'))

    def set_credits(self, person, amount):
        self.flag_service.set_flag_value('coffee_beer', person, 'credits', int(amount))
