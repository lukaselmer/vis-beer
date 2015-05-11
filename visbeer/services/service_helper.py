import re
import datetime

ENABLE_BEER_CONSUMPTION = True
DEFAULT_CREDITS_PER_DAY = 2
RFID_REGEX = re.compile(r"[0-9]{6}@rfid\.ethz\.ch")


def beginning_of_current_day():
    cutoff = datetime.time(3, 0)
    if datetime.datetime.now().time() < cutoff:
        day = datetime.date.today() - datetime.timedelta(days=1)
    else:
        day = datetime.date.today()
    return datetime.datetime.combine(day, cutoff)


def validate_rfid(rfid):
    if not RFID_REGEX.match(rfid):
        raise Exception('Invalid rfid')

