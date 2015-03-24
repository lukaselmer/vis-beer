class BeerServiceMock:
    lastRfidCallStatus = ''
    lastRfidCallDispensed = ''

    def __init__(self, rfid):
        self.rfid = rfid

    def status(self):
        BeerServiceMock.lastRfidCallStatus = self.rfid
        if self.rfid == '010101@rfid.ethz.ch':
            return '1'
        elif self.rfid == '020202@rfid.ethz.ch':
            return '2'
        raise 'bad value'

    def dispensed(self):
        BeerServiceMock.lastRfidCallDispensed = self.rfid
        return '77'
