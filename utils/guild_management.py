import discord
from discord import Member
from discord import Guild

from utils import mongo

## TODO: Improve functionality if denoted welcome channel not found
async def welcome_user(member: Member):
    WELCOME_MESSAGE = f"Welcome to {member.guild.name}, {member.mention}"

    welcome_channel = discord.utils.find(
        lambda g: g.name=='general' and isinstance(g, discord.TextChannel), member.guild.channels
    )
    if welcome_channel:
        await welcome_channel.send(content=WELCOME_MESSAGE)
    else:
        await member.create_dm()
        await member.dm_channel.send(content=WELCOME_MESSAGE)

async def on_join(guild: Guild):
    mongo.add_guild(guild)

async def on_remove(guild: Guild):
    mongo.remove_guild(guild)