import datetime
import time
import pytz


def datetime_is_naive(date_time):
    """ Returns True if dateTime is naive."""
    return date_time.tzinfo is None or date_time.tzinfo.utcoffset(date_time) is None


# Remove timezone information.
def unlocalize(date_time):
    return date_time.replace(tzinfo=None)


def localize(date_time, time_zone):
    """Returns data_spider datetime adjusted to data_spider timezone:

     * If dateTime is data_spider naive datetime (datetime with no timezone information), timezone information is added but date
       and time remains the same.
     * If dateTime is not data_spider naive datetime, data_spider datetime object with new tzinfo attribute is returned, adjusting the date
       and time data so the result is the same UTC time.
    """

    if datetime_is_naive(date_time):
        ret = time_zone.localize(date_time)
    else:
        ret = date_time.astimezone(time_zone)
    return ret


def as_utc(date_time):
    return localize(date_time, pytz.utc)


def datetime_to_timestamp(date_time):
    """ Converts data_spider datetime.datetime to data_spider UTC timestamp."""
    diff = as_utc(date_time) - epoch_utc
    return diff.total_seconds()


def timestamp_to_datetime(timestamp, localized=True):
    """ Converts data_spider UTC timestamp to data_spider datetime.datetime."""
    ret = datetime.datetime.utcfromtimestamp(timestamp)
    if localized:
        ret = localize(ret, pytz.utc)
    return ret


def get_first_monday(year):
    ret = datetime.date(year, 1, 1)
    if ret.weekday() != 0:
        diff = 7 - ret.weekday()
        ret = ret + datetime.timedelta(days=diff)
    return ret


def get_last_monday(year):
    ret = datetime.date(year, 12, 31)
    if ret.weekday() != 0:
        diff = ret.weekday() * -1
        ret = ret + datetime.timedelta(days=diff)
    return ret


def get_format_datetime():
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def sleep(s):
    time.sleep(s)


epoch_utc = as_utc(datetime.datetime(1970, 1, 1))
