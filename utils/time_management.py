from datetime import datetime, timezone, timedelta
import pytz
import asyncio
from dateutil import parser

from utils.mongo import MONGODB_URI
from utils import mongo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores import mongodb
from apscheduler.triggers.date import DateTrigger

from discord import TextChannel

## Set up scheduler
store = mongodb.MongoDBJobStore(client=mongo.client, collection='reminders')
print(store)
scheduler = AsyncIOScheduler(timezone='utc', jobstores={'mongodb':store})

## Will create a time interval from now to the specified number of 
# days in the future
def create_window(delta=20):
    today = datetime.now(timezone.utc)
    tomorrow = today + timedelta(days=delta)

    return (today, tomorrow)

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

async def send_reminder(reminder: str, channel: TextChannel):
    await channel.send(reminder)

async def schedule(event_time, event_name, channel: TextChannel):
    return scheduler.add_job(
        func=send_reminder, trigger=DateTrigger(event_time, 'utc'), args=(event_name, channel), 
        id=str(channel)+event_name
    )