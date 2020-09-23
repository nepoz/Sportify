import os 
from dotenv import load_dotenv
import typing
import requests
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context

from discord.ext.commands.errors import CommandInvokeError
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext.commands.errors import UserInputError
from discord.ext.commands.errors import CommandNotFound
from pytz.exceptions import UnknownTimeZoneError

from utils import guild_management
from utils import time_management

import command_handlers
from command_handlers import esports
from command_handlers import guild
from command_handlers import sports
from command_handlers import help

from error_handlers import time_errors
from error_handlers import argument_errors

## Set up error logger
logging.basicConfig()

## load Discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

## Create bot client, remove default help command
bot = commands.Bot(command_prefix="^")
bot.remove_command('help')

## Test to see if bot can run
@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord")
    logging.info(f"The bot is currently in guilds: {bot.guilds}")
    print(time_management.scheduler.get_jobs())

## Create database entry for guild when joining new guild
@bot.event
async def on_guild_join(guild):
    await guild_management.on_join(guild)

## Remove guild and associated data from DB when removed from guild
@bot.event
async def on_guild_remove(guild):
    await guild_management.on_remove(guild)

## Handles uknown command exceptions
@bot.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, CommandNotFound):
        await argument_errors.not_command(ctx, error)


## Handler for csgo related queries
@bot.command(name="csgo")
async def csgo(ctx, timezone=None):
    await esports.get_csgo_schedule(ctx, timezone)
@csgo.error
async def csgo_error(ctx: Context, error):
    if isinstance(error.__cause__, UnknownTimeZoneError):
        await time_errors.invalid_tz(ctx, error)
    else:
       await argument_errors.default(ctx, error)

@bot.command(name="csgo3day")
async def csgo3day(ctx, timezone=None):
    await esports.get_csgo_schedule(ctx, timezone, three_day=True)
@csgo3day.error
async def csgo3day_error(ctx: Context, error):
    if isinstance(error.__cause__, UnknownTimeZoneError):
        await time_errors.invalid_tz(ctx, error)
    else:
        await argument_errors.default(ctx, error)

@bot.command(name="sport")
async def sport(ctx, league, timezone=None):
    await sports.get_sport_schedule(ctx, league, timezone)
@sport.error
async def sport_error(ctx: Context, error):
    if isinstance(error, MissingRequiredArgument):
        await argument_errors.sport(ctx, error)
    elif isinstance(error.__cause__, UnknownTimeZoneError):
        await time_errors.invalid_tz(ctx, error)
    else:
        await argument_errors.default(ctx, error)

@bot.command(name="sport3day")
async def sport3day(ctx, league, timezone=None):
    await sports.get_sport_schedule(ctx, league, timezone, three_day=True)
@sport3day.error
async def sport3day_error(ctx: Context, error):
    if isinstance(error, MissingRequiredArgument):
        await argument_errors.sport(ctx, error)
    elif isinstance(error.__cause__, UnknownTimeZoneError):
        await time_errors.invalid_tz(ctx, error)
    else:
        await argument_errors.default(ctx, error)

@bot.command(name="set_tz")
async def set_tz(ctx: Context, timezone):
    await command_handlers.guild.set_tz(ctx, timezone)
@set_tz.error
async def set_tz_error(ctx:Context, error):
    if isinstance(error, MissingRequiredArgument):
        await argument_errors.set_tz(ctx, error)
    elif isinstance(error.__cause__, UnknownTimeZoneError):
        await time_errors.invalid_tz(ctx, error)
    else:
        await argument_errors.default(ctx, error)

@bot.command(name="get_tz")
async def get_tz(ctx: Context):
    await command_handlers.guild.get_tz(ctx)
@get_tz.error
async def get_tz_error(ctx:Context, error):
    await argument_errors.default(ctx, error)

@bot.command(name="help")
async def get_help(ctx: Context, command='help'):
    await help.help(ctx, command)
@get_help.error
async def get_help_error(ctx: Context, error):
    if isinstance(error, UserInputError):
        await argument_errors.not_command(ctx, error)
    else:
        await argument_errors.default(ctx, error)

## Start bot
bot.run(DISCORD_TOKEN)
