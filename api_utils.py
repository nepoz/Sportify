from datetime import datetime, timezone, timedelta
import pytz

## Will create a time interval from now to the specified number of 
# days in the future
def generate_time_window(delta=1):
    today = datetime.now(timezone.utc)
    tomorrow = today + timedelta(days=delta)

    return (today.isoformat(), tomorrow.isoformat())

def convert_to_timezone(usr_datetime: datetime, user_tz):
    usr_utc = usr_datetime.replace(tzinfo=timezone.utc)
    return usr_utc.astimezone(pytz.timezone(user_tz))

def clean_datetime  (user_datetime):
    fmt = fmt = "%Y-%m-%d %H:%M"
    return user_datetime.strftime(fmt)