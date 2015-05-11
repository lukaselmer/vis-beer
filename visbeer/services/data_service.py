class DataService:
    def __init__(self, flag_service):
        self.flag_service = flag_service

    def find_person(self, rfid):
        return self.flag_service.find_person(rfid)

    def get_beer_no_limit(self, person):
        return self.flag_service.get_flag_value('beer', person, 'nolimit')

    def get_beer_per_day(self, person):
        return self.flag_service.get_flag_value('beer', person, 'perday')

    def set_default_beers_per_day(self, person, default):
        self.flag_service.set_default_flag_value('beer', person, 'perday', default)

    def get_beer_remaining(self, person):
        return self.flag_service.get_flag_value('beer', person, 'remaining')

    def set_beer_remaining(self, person, amount):
        self.flag_service.set_flag_value('beer', person, 'remaining', amount)

    def get_beer_dispensed_today(self, person):
        return self.flag_service.get_flag_value('beer', person, 'dispensed_today')

    def get_beer_last(self, person):
        return self.flag_service.get_flag_value('beer', person, 'last')

    def set_beer_last(self, person, last_time):
        self.flag_service.set_flag_value('beer', person, 'last', last_time)
