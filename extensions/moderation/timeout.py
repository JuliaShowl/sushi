from tokenize import String
from datetime import datetime, timedelta
import lightbulb
import hikari
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from pytz import timezone

PUNISHMENTS = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('timeout')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)
PERMISSIONS = (
    hikari.Permissions.MODERATE_MEMBERS
)

@plugin.command()
@lightbulb.option("reason", "the reason for the timeout", str, required=False,default='Not specified')
@lightbulb.option("days", "the duration of the timeout (days)", int, required=False, default=0)
@lightbulb.option("hour", "the duration of the timeout (hour)", int, required=False, default=0)
@lightbulb.option("minute", "the duration of the timeout (minute)", int, required=False, default=0)
@lightbulb.option("second", "the duration of the timeout (second)", int, required=False, default=0)
@lightbulb.option("user", "the user you want to be put in timeout", required=True)
@lightbulb.command("timeout", "Timeout a member", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout(ctx: lightbulb.Context, user: hikari.Member, second: int, minute: int, hour: int , days: int, reason: str):
    
    user_id = ctx.options.user.replace('<','').replace('>','').replace('@','')
    username = await ctx.bot.rest.fetch_user(user_id)

    now = datetime.now()
    then = now + timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    
    if (then - now).days > 28:
        await ctx.respond("You can't time someone out for more than 28 days")
        return
    
    if days == 0 and hour == 0 and minute == 0 and second == 0:
        await ctx.respond(f"Removing timeout from **{username}**")
        txt = f"Timeout for {username} has been removed successfully!"
    else:
        await ctx.respond(f"Attempting to timeout **{username}**")
        txt = f"{username} has been timed out until <t:{int(then.timestamp())}:R> for `{ctx.options.reason}`"
        try:
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()
            rng = 'Sheet1!A:A'

            # How the input data should be interpreted.
            value_input_option = 'USER_ENTERED'

            value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [[str(now.strftime("%Y-%m-%d %H:%M:%S"))] ,["Timeout"], [str(username)], [str(user_id)], [str(ctx.options.reason)], [str(then-now)]]
            }

            sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

        except HttpError as err:
            print(err)
    
    await ctx.bot.rest.edit_member(user = user_id, guild = ctx.get_guild(), communication_disabled_until=then, reason=ctx.options.reason)
    await ctx.edit_last_response(txt)

def load(bot):
    bot.add_plugin(plugin)
