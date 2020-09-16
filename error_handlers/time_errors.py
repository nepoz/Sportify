from discord.ext.commands import errors
from discord.ext.commands import Context
import logging

async def invalid_tz(ctx: Context, error):
    if isinstance(error, errors.CommandInvokeError):
        await ctx.send("Did not find that timezone! Check valid timezones here: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")
        logging.error(error)