from visbeer.test.mocks.person_mock import PersonMock

class DataServiceMock:
    def find_person(self, rfid):
        return PersonMock()

    def flag_values(self, person):
        return None
