import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime

def getTimeZone(city):
    geolocator = Nominatim(user_agent="Any Name")
    tf = TimezoneFinder()
    cords = geolocator.geocode(city)
    timezone = tf.timezone_at(lng = cords.longitude, lat= cords.latitude)
    return timezone

def convertTime(prev_city, next_city, time):
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
    date = list(map(int, date.split("/")))
    time = list(map(int, time.split(":")))
    obj = datetime.datetime(date[2], date[1], date[0], time[0], time[1])
    return obj