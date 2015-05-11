from visbeer.test.mocks.person_mock import PersonMock


class FlagServiceMock:
    def __init__(self):
        self.data = {'persons': {}}

    def find_person(self, rfid):
        if rfid not in self.data['persons']:
            self.data['persons'][rfid] = PersonMock(rfid)
        return self.data['persons'][rfid]

    def get_flag_value(self, flag_group, person, flag_name):
        res = self._get_person_data(person).get(flag_group + '|' + flag_name, None)
        return res if res is None else str(res)

    def set_flag_value(self, flag_group, person, flag_name, new_value):
        self._get_person_data(person)[flag_group + '|' + flag_name] = new_value

    def set_default_flag_value(self, flag_group, person, flag_name, new_default_value):
        if not self.get_flag_value(flag_group, person, flag_name):
            self.set_flag_value(flag_group, person, flag_name, new_default_value)

    def _get_person_data(self, person):
        if person.rfid not in self.data:
            self.data[person.rfid] = {}
        return self.data[person.rfid]
