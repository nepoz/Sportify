import discord 

## TODO: some sort of type restriction on member using types?

async def welcome(member):
    await member.create_dm()
    await member.dm_channel.send(f"Testing welcome function!")