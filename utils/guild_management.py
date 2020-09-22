import discord
from discord import Member
from discord import Guild

from utils import mongo

async def on_join(guild: Guild):
    mongo.add_guild(guild)
    
    ## Let everyone know the bot is here!
    for c in guild.text_channels:
        await c.send("Thanks for the invite! Use ^help to see a list of available commands.")

async def on_remove(guild: Guild):
    mongo.remove_guild(guild)