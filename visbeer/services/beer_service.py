import re

RFID_REGEX = re.compile(r"[0-9]{6}@rfid\.ethz\.ch")


class BeerService:
    def validate_rfid(rfid):
        if not RFID_REGEX.match(rfid):
            raise Exception('Invalid rfid')

    def __init__(self, rfid):
        BeerService.validate_rfid(rfid)
        self.rfid = rfid

    def status(self):
        return 'TODO'

    def dispensed(self):
        return 'TODO'
