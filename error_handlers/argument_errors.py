from discord.ext.commands import Context
import logging

async def default(ctx: Context, error):
    await ctx.send("Oopsie daisies, don't really know what you wanted me to do.")
    logging.exception(error)

async def sport(ctx: Context, error):
    await ctx.send("Indicate what league you want the schedule for! Like: ^sport nba")
    logging.exception(error)

async def set_tz(ctx: Context, error):
    await ctx.send("Indicate what timezone you want! Like: ^set_tz US/Central")
    logging.error(error)

async def not_command(ctx: Context, error):
    await ctx.send("Did not recognize command, use ^help to see list of available commands.")
    logging.error(error)