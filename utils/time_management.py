from datetime import datetime, timezone, timedelta
import pytz
import asyncio
from dateutil import parser

from utils.mongo import MONGODB_URI
from utils import mongo

from discord import TextChannel
from discord.ext.commands import Bot


## Will create a time interval from now to the specified number of 
# days in the future
def create_window(delta=20):
    today = datetime.now(timezone.utc)
    future = today + timedelta(days=delta)

    return (today, future)

## Converts given datetime to a specified timezone
def to_tz(usr_datetime: datetime, user_tz='utc'):
    usr_dt = usr_datetime.replace(tzinfo=pytz.utc) if not usr_datetime.tzinfo else usr_datetime
    return usr_dt.astimezone(pytz.timezone(user_tz))

## Formats datetime to standard readable format
def readify(usr_datetime: datetime):
    fmt = "%Y-%m-%d %H:%M"
    return usr_datetime.strftime(fmt)

## Checks if user tz can be used in pytz.timezone()
def validate(user_tz):
    return user_tz.lower() in (tz.lower() for tz in pytz.all_timezones_set)

## Create utc datetime for SportsDB events
def create_utcdatetime(event_date, event_time):
    dt = " ".join([event_date, event_time])
    parsed = parser.parse(dt)
    return parsed.replace(tzinfo=pytz.utc)