import discord
import os 
from dotenv import load_dotenv

## load Discord token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

## Start bot client
client = discord.Client()

## Test to see if bot can run
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord")
    print(f"The bot is currently in guilds: {client.guilds}")

## Start bot
client.run(TOKEN)
