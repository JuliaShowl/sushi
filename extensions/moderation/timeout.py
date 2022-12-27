from tokenize import String
from datetime import datetime, timedelta
import lightbulb
import hikari
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

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

@plugin.command()
@lightbulb.option("reason", "Reason for timeout", type=str, required=False,default='Not specified')
@lightbulb.option("days", "Duration of the timeout (days)", type=int, required=False, default=0)
@lightbulb.option("hour", "Duration of the timeout (hour)", type=int, required=False, default=0)
@lightbulb.option("minute", "Dration of the timeout (minute)", type=int, required=False, default=0)
@lightbulb.option("second", "Duration of the timeout (second)", type=int, required=False, default=0)
@lightbulb.option("user", "The user to timeout", type=hikari.User,required=True)
@lightbulb.command("timeout", "Timeout a user, will attempt to remove timeout from user if no duration is specified", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout(ctx: lightbulb.Context, user: hikari.User, second: int, minute: int, hour: int , days: int, reason: str):
    now = datetime.now(tz=pytz.UTC)
    then = now + timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    
    if (then - now).days > 28:
        await ctx.respond("You can't time someone out for more than 28 days")
        return
    
    if days == 0 and hour == 0 and minute == 0 and second == 0:
        await ctx.respond(f"Removing timeout from **{user}**")
        txt = f"Timeout for {user} has been removed successfully!"
    else:
        await ctx.respond(f"Attempting to timeout **{user}**")
        txt = f"{user} has been timed out until <t:{int(then.timestamp())}:R> for `{ctx.options.reason}`"
        try:
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()
            rng = 'Sheet1!A:A'

            # How the input data should be interpreted.
            value_input_option = 'USER_ENTERED'

            value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [[str(now.strftime("%Y-%m-%d %H:%M:%S"))] ,["Timeout"], [str(user)], [str(user.id)], [str(ctx.options.reason)], [str(ctx.author)], [str(then-now)]]
            }

            sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

        except HttpError as err:
            print(err)
    
    await ctx.bot.rest.edit_member(user = user.id, guild = ctx.get_guild(), communication_disabled_until=then, reason=reason)
    await ctx.edit_last_response(txt)

def load(bot):
    bot.add_plugin(plugin)
