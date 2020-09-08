import os 
from dotenv import load_dotenv
import typing
import requests
from discord.ext.commands.errors import CommandInvokeError
from discord.ext.commands.errors import MissingRequiredArgument

import discord
from discord.ext import commands
from discord.ext.commands import Context

from utils import guild_management
from utils import time_management

import command_handlers
from command_handlers import esports
from command_handlers import guild
from command_handlers import sports

from error_handlers import time_errors

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
    guild_management.on_join(guild)

## Remove guild and associated data from DB when removed from guild
@bot.event
async def on_guild_remove(guild):
    guild_management.on_remove(guild)

## Welcomes user to the guild
@bot.event
async def on_member_join(member: discord.Member):
    await guild_management.welcome_user(member)

## Handler for csgo related queries
@bot.command(name="csgo")
async def csgo(ctx, timezone=None):
    await esports.get_csgo_schedule(ctx, timezone)
# @csgo.error
# async def csgo_error(ctx: Context, error):
#     print (error)
#     await time_errors.invalid_tz(ctx, error)

@bot.command(name="csgo3day")
async def csgo3day(ctx, timezone=None):
    await esports.get_csgo_schedule(ctx, timezone, three_day=True)
@csgo3day.error
async def csgo3day_error(ctx: Context, error):
    await time_errors.invalid_tz(ctx, error)

@bot.command(name="sport")
async def sport(ctx, league, timezone=None):
    await sports.get_sport_schedule(ctx, league, timezone)
@sport.error
async def sports_error(ctx: Context, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Indicate what league you want the schedule for! Like: ^sport nba")

@bot.command(name="set_tz")
async def set_tz(ctx: Context, timezone):
    await command_handlers.guild.set_tz(ctx, timezone)

@bot.command(name="get_tz")
async def get_tz(ctx: Context):
    await command_handlers.guild.get_tz(ctx)

## Start bot
bot.run(DISCORD_TOKEN)
