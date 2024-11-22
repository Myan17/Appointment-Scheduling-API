import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime

def getTimeZone(city):
    """
    Get the timezone of a given city.

    Args:
        city (str): Name of the city.

    Returns:
        str: The timezone name of the city.

    Raises:
        ValueError: If the city's coordinates cannot be determined.
    """
    geolocator = Nominatim(user_agent="Any Name")
    tf = TimezoneFinder()
    cords = geolocator.geocode(city)
    timezone = tf.timezone_at(lng = cords.longitude, lat= cords.latitude)
    return timezone

def convertTime(prev_city, next_city, time):
    """
    Convert the time from one city's timezone to another.

    Args:
        prev_city (str): Timezone name of the starting city.
        next_city (str): Timezone name of the destination city.
        time (datetime): The time in the starting city's timezone.

    Returns:
        str: The converted time in the format "dd/mm/yy,HH:MM".

    Raises:
        UnknownTimeZoneError: If either of the timezones cannot be determined.
    """
    old_time = time
    prev_city_timeZone = prev_city
    next_city_timeZone = next_city
    tz = pytz.timezone(prev_city_timeZone)
    old_time = tz.localize(old_time)
    next_timezone = pytz.timezone(next_city_timeZone)
    next_tz_time = old_time.astimezone(next_timezone)
    print(next_tz_time.strftime("%M"))
    return next_tz_time.strftime("%d/%m/%y,%H:%M")

def getTime(date, time):
    """
    Combine a date and time string into a datetime object.

    Args:
        date (str): The date in "dd/mm/yyyy" format.
        time (str): The time in "HH:MM" format.

    Returns:
        datetime: The combined datetime object.

    Raises:
        ValueError: If the input date or time format is invalid.
    """
    date = list(map(int, date.split("/")))
    time = list(map(int, time.split(":")))
    obj = datetime.datetime(date[2], date[1], date[0], time[0], time[1])
    return obj
