from dateutil import parser
import dateutil.tz

def parse_timezone(date_str, timezone='UTC'):
    date = parser.parse(date_str)
    return date.astimezone(dateutil.tz.gettz(timezone))
