

import datetime
import time


def convert_unix_date_time_to_utc_date_time(unix_date_time):
    return datetime.datetime.utcfromtimestamp(unix_date_time)

# Convert datetime object to Unix timestamp
# the weather API uses Unix timestamp
def convert_utc_date_time_to_unix_date_time(utc_date_time):
    return time.mktime(utc_date_time.timetuple())