from tokenize import String
from datetime import datetime, timedelta
import lightbulb
import hikari
import pytz
from time import sleep

plugin = lightbulb.Plugin('faketimeout')

@plugin.command()
@lightbulb.add_cooldown(5.0,1,lightbulb.UserBucket)
@lightbulb.option("reason", "Reason for timeout", type=str, required=False,default='Not specified')
@lightbulb.option("days", "Duration of the timeout (days)", type=int, required=False, default=0)
@lightbulb.option("hour", "Duration of the timeout (hour)", type=int, required=False, default=0)
@lightbulb.option("minute", "Dration of the timeout (minute)", type=int, required=False, default=0)
@lightbulb.option("second", "Duration of the timeout (second)", type=int, required=False, default=0)
@lightbulb.option("user", "The user to timeout", type=hikari.User,required=True)
@lightbulb.command("timeouts", "Timeout a user, will attempt to remove timeout from user if no duration is specified", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def timeouts(ctx: lightbulb.Context, user: hikari.User, second: int, minute: int, hour: int , days: int, reason: str):
    now = datetime.now(tz=pytz.timezone("Asia/Seoul"))
    then = now + timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    
    if (then - now).days > 28:
        await ctx.respond("You can't time someone out for more than 28 days")
        return
    
    if days == 0 and hour == 0 and minute == 0 and second == 0:
        await ctx.respond(f"Removing timeout from **{user}**")
        txt = f"Timeout for {user} has been removed successfully!"
        sleep(1)
        await ctx.edit_last_response(txt)
        return

    else:
        await ctx.respond(f"Attempting to timeout **{user}**")
        sleep(1)
        txt = f"{user.mention} has been timed out until <t:{int(then.timestamp())}:R> for `{ctx.options.reason}`"
        await ctx.edit_last_response(txt)

def load(bot):
    bot.add_plugin(plugin)
