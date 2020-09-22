from discord.ext.commands import Context
import json
from discord.ext.commands.errors import UserInputError

with open('utils/COMMANDS.json') as f:
    HELP_TEXT: dict = json.load(f)
    f.close()

async def help(ctx: Context, command: str = 'help'):
    command = command.lower()
    if command not in HELP_TEXT:
        raise UserInputError

    if command == "help":
        out: str = "\n\n".join(HELP_TEXT.values())
    elif command == "sport":
        out: str = "\n\n".join((HELP_TEXT[command], HELP_TEXT[f"{command}3day"]))
    elif command == "csgo":
        out: str = "\n\n".join((HELP_TEXT[command], HELP_TEXT[f"{command}3day"]))
    else:
        out: str = HELP_TEXT[command]
    
    out = "```" + out + "```"
    await ctx.send(out)