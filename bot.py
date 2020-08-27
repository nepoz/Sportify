import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv
import typing

## load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

## Start bot client
bot = commands.Bot(command_prefix="^")

## Test to see if bot can run
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord")
    print(f"The bot is currently in guilds: {bot.guilds}")

## Test to see if we can welcome a user in #general chat
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

## Start bot
bot.run(TOKEN)
