import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv
import typing
from api_utils import generate_24_hour_window, convert_to_timezone, clean_datetime
import requests
from datetime import datetime, timezone

## load Discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PANDA_TOKEN = os.getenv('PANDA_TOKEN')

## Auth headers for API Calls
PANDA_AUTH = {"Authorization" : f"Bearer {PANDA_TOKEN}"}

## Create bot client
bot = commands.Bot(command_prefix="^")

## Test to see if bot can run
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord")
    print(f"The bot is currently in guilds: {bot.guilds}")

## Create database entry for guild when joining new guild
@bot.event
async def on_guild_join(guild):
    pass

## Remove guild and associated data when removed from guild
@bot.event
async def on_guild_remove(guild):
    pass

## Welcomes user to the guild
@bot.event
async def on_member_join(member: discord.Member):
    WELCOME_MESSAGE = f"Welcome to {member.guild.name}, {member.mention}"

    welcome_channel = discord.utils.find(
        lambda g: g.name=='general' and isinstance(g, discord.TextChannel), member.guild.channels
    )
    if welcome_channel:
        await welcome_channel.send(content=WELCOME_MESSAGE)
    else:
        await member.create_dm()
        await member.dm_channel.send(content=WELCOME_MESSAGE)

## List upcoming A or S tier CSGO games
# TODO: Add customization for time period to check
# TODO: Add functionality for added arguments eg. upcoming, tournaments etc.  
# TODO: Add functionality to look a specified time ahead in the future
@bot.command(name="csgo")
async def get_csgo_schedule(ctx, timezone='utc'):
    async with ctx.typing():
        r = requests.get(
            url='https://api.pandascore.co/csgo/matches/upcoming',
            headers=PANDA_AUTH,
            params = {
                'per_page' : 100,
                'range[begin_at]' : ', '.join(generate_24_hour_window()),
            }
        )

        games = r.json()
        games_to_show = [game for game in games if game['serie']['tier']=='a' or game['serie']['tier']=='s']
        
        display = [{ 
            'tournament' : game['serie']['full_name'], 
            'game_name' : game["name"],
            'game_time' : convert_to_timezone(datetime.fromisoformat(game["begin_at"][:-1]), timezone) 
            } 
            for game in games_to_show
        ]

        output = 'Upcoming CSGO Matches:\n'
        for item in display:
            output += (f"```Tournament : {item['tournament']}\nGame: {item['game_name']}\nTime: {clean_datetime(item['game_time'])}\n```")

        await ctx.send(output)


## Start bot
bot.run(DISCORD_TOKEN)
