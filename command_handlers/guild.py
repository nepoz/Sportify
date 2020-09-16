from pytz.exceptions import UnknownTimeZoneError

from discord.ext.commands import Context

from utils import time_management
from utils import mongo

async def set_tz(ctx: Context, timezone):
    if time_management.validate(timezone):
        mongo.update_guild_timezone(ctx.guild, timezone.lower())
        await ctx.send(f"Timezone now set to `{timezone.lower()}`")
    else:
        raise UnknownTimeZoneError

async def get_tz(ctx: Context):
    tz = mongo.get_guild_tz(ctx.guild)
    await ctx.send(f"The guild's timezone is currently set to `{tz}`")