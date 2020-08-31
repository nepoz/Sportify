import os
import dotenv
from pymongo import MongoClient
from discord import Guild

dotenv.load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.sportify

def add_guild(guild: Guild):
    new_guild = {
        "name": guild.name,
        "guild_id" : guild.id,
        "timezone" : "utc"
    }

    return db.guilds.insert_one(new_guild)

def update_guild_timezone(guild: Guild, valid_tz):
    return (
        db.guilds.update_one({"guild_id" : guild.id}, {"$set" : {'timezone' : valid_tz}})
    )

def remove_guild(guild: Guild):
    return db.guilds.remove({"guild_id" : guild.id})

def get_guild_tz(guild: Guild):
    target = db.guilds.find_one({"guild_id" : guild.id})
    return target["timezone"]