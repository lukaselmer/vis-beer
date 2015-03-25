class DataService:
    def __init__(self):
        pass

    def find_person(self, rfid):
        # TODO: implement this, use vislib
        return None

    def get_flag_value(self, person, flag_name):
        # TODO: implement this, use flags
        return None

    def set_flag_value(self, person, flag_name, new_value):
        # TODO: implement this, use flags
        return None

    def set_default_flag_value(self, person, flag_name, new_default_value):
        if not self.get_flag_value(person, flag_name):
            self.set_flag_value(person, flag_name, new_default_value)
