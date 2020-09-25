import requests
from datetime import datetime
from datetime import timedelta
import pytz
import json
import asyncio

from utils import time_management
from utils import mongo

from discord.ext.commands import Context
from discord import Message

with open('utils/SDB_IDS.json', 'r') as f:
    SDB_IDS = json.load(f)

## Helper function to extract 15 events as returned by SDB
async def extract_15(league, timezone, three_day):
    r = requests.get(
        url=f"https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={SDB_IDS[league.lower()]}",
    )

    next15 = r.json()['events']

    ## if we can't find any events, then return None
    if not next15:
        return None
    
    if three_day:
        three_day_window = time_management.create_window(3)
        to_show = [
            game for game in next15 if 
            time_management.create_utcdatetime(game['dateEvent'], game['strTime'])
            <= three_day_window[1]
        ]
    else:
        to_show = next15

    ## Filter out games that have already taken place
    upcoming_games = [
        game for game in to_show if 
        time_management.create_utcdatetime(game['dateEvent'], game['strTime'])
        >= datetime.now().astimezone(pytz.utc)
    ]

    display = [{
        'match' : game['strEvent'],
        'game_time' : time_management.to_tz(
            time_management.create_utcdatetime(game['dateEvent'], game['strTime']),
            timezone),
        'item_number' : i + 1
    } for i, game in enumerate(upcoming_games)]
    
    return display

async def get_sport_schedule(ctx: Context, league, timezone, three_day=False):
    bot = ctx.bot
    await ctx.channel.trigger_typing()
    
    if not timezone:
        timezone = mongo.get_guild_tz(ctx.guild)
    
    display = await extract_15(league, timezone, three_day)
    
    output = f"Upcoming {league.upper()} Matches:\n" if not three_day else f"Upcoming {league.upper()} \
        matches in next 3 days:"
    no_games = f"No {league.upper()} matches found for specified period."

    if not display:
        await ctx.send(no_games)
    else:
        for item in display:
            output += (f"```{item['item_number']}. {item['match']}\n")
            output += f"Time: {time_management.readify(item['game_time'])}\n```"
        await ctx.send(output)
        await ctx.send("If you want to set a reminder for an event, send the event number in next 45 seconds.")

        def range_check(m: Message):
            return int(m.content) in range(len(display) + 1) and m.author == ctx.author

        try: 
            reminder_for = await bot.wait_for('message', check=range_check, timeout=45)
            index = int(reminder_for.content) - 1
            time = time_management.to_tz(display[index]['game_time'], 'utc')
            match = display[index]['match']
        except asyncio.TimeoutError:
            await ctx.send('Did not register a selection')
        else:
            return (time, match)
