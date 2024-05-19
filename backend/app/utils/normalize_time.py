from dateutil import parser
import dateutil.tz
 
# We parse a date from a string and convert it to a different timezone
# By default, the timezone will be chilean time
def parse_timezone(date_str, timezone='Chile/Continental'):
    date = parser.parse(date_str)
    return date.astimezone(dateutil.tz.gettz(timezone))