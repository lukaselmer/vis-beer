from visbeer.test.mocks.person_mock import PersonMock


class DataServiceMock:
    def __init__(self):
        self.data = {'persons': {}}

    def find_person(self, rfid):
        if not rfid in self.data['persons']:
            self.data['persons'] = PersonMock(rfid)
        return self.data['persons']

    def get_flag_value(self, person, flag_name):
        res = self.get_person_data(person).get(flag_name, None)
        return res if res is None else str(res)

    def set_flag_value(self, person, flag_name, new_value):
        self.get_person_data(person)[flag_name] = new_value

    def set_default_flag_value(self, person, flag_name, new_default_value):
        if not self.get_flag_value(person, flag_name):
            self.set_flag_value(person, flag_name, new_default_value)

    def get_person_data(self, person):
        if not person.rfid in self.data:
            self.data[person.rfid] = {}
        return self.data[person.rfid]
