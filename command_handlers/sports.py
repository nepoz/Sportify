import requests
from datetime import datetime
import json

from utils import time_management
from utils import mongo

from discord.ext.commands import Context
from pprint import pprint

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

    display = [{
        'match' : game['strEvent'],
        'game_time' : time_management.to_tz(
            time_management.create_utcdatetime(game['dateEvent'], game['strTime']),
            timezone),
        'item_number' : i + 1
    } for i, game in enumerate(to_show)]
    
    return display

async def get_sport_schedule(ctx: Context, league, timezone, three_day=False):
    async with ctx.typing():
        if not timezone:
            timezone = mongo.get_guild_tz(ctx.guild)
        
        display = await extract_15(league, timezone, three_day)

        output = f"Upcoming {league.upper()} Matches:\n" if not three_day else f"Upcoming {league.upper()} matches in next 3 days:"
        no_games = f"No {league.upper()} matches found for specified period."

        if not display:
            await ctx.send(no_games)
        else:
            for i, item in enumerate(display):
                output += (f"```{item['item_number']}. {item['match']}\n")
                output += f"Time: {time_management.readify(item['game_time'])}\n```"
            await ctx.send(output)