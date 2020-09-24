import os
import dotenv
import requests
from datetime import datetime
import asyncio

from utils import time_management
from utils import mongo

from discord.ext.commands import Context
from discord import Message

dotenv.load_dotenv()
PANDA_TOKEN = os.getenv('PANDA_TOKEN')

PANDA_AUTH = {"Authorization" : f"Bearer {PANDA_TOKEN}"}

## List upcoming A or S tier CSGO games
# TODO: Add customization for time period to check
# TODO: Add functionality for added arguments eg. upcoming, tournaments etc.  
# TODO: Add functionality to look a specified time ahead in the future
async def get_csgo_schedule(ctx: Context, timezone, three_day=False):
    bot = ctx.bot
    await ctx.channel.trigger_typing()
    
    if not timezone:
        timezone = mongo.get_guild_tz(ctx.guild)

    window = [
        t.isoformat() for t in time_management.create_window(3)
    ] if three_day else None
    
    r = requests.get(
        url='https://api.pandascore.co/csgo/matches/upcoming',
        headers=PANDA_AUTH,
        params = {
            'per_page' : 100,
            'range[begin_at]' : ', '.join(window) if three_day else None  
        }
    )

    games = r.json()
    games_to_show = [game for game in games if game['serie']['tier']=='a' or game['serie']['tier']=='s'][:15]
    
    display = [{ 
        'tournament' : game['serie']['full_name'], 
        'match' : game["name"],
        'game_time' : time_management.to_tz(datetime.fromisoformat(game["begin_at"][:-1]), timezone),
        'item_number' : i + 1 
        } 
        for i, game in enumerate(games_to_show)
    ]

    output = 'Next top tier CSGO Matches I found:\n' if not three_day else "CSGO matches in the next three days:\n"
    no_games = "No top tier CS games found for specified period."

    for item in display:
        output += (f"```{item['item_number']}. Tournament : {item['tournament']}\n")
        output += f"Match: {item['match']}\n"
        output += f"Time: {time_management.readify(item['game_time'])}\n```"

    if not display:
        await ctx.send(no_games)
    else:
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
            await ctx.send(f"Okay! Reminder set for {match}!")
            await time_management.schedule(time, match, ctx.channel.id)
