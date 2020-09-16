from discord.ext.commands import Context
import json

with open('utils/COMMANDS.json') as f:
    HELP_TEXT = json.load(f)
    f.close()

async def help(ctx: Context, command: str = 'help'):
    await ctx.send(HELP_TEXT[command])