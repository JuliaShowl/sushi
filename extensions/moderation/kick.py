from tokenize import String
from datetime import datetime
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

plugin = lightbulb.Plugin('kick')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.KICK_MEMBERS),
    lightbulb.guild_only
)

@plugin.command()
@lightbulb.option("reason", "Reason for kicking member", type=str, required=False, default="Not specified")
@lightbulb.option("user", "User you want to kick", type=hikari.User,required=True)
@lightbulb.command("kick", "Kick a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context, user: hikari.User, reason: str):
    await ctx.bot.rest.kick_member(user = user.id, guild = ctx.get_guild(), reason = reason)
    dt = datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        rng = 'Sheet1!A:A'

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'

        value_range_body = {
            "majorDimension": "COLUMNS",
           'values': [[str(dt)] ,["Kick"], [str(user)], [str(user.id)], [str(reason)], [str(ctx.author)]]
        }

        sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    await ctx.respond(f"{user} has been kicked for `{reason}`")
    

def load(bot):
    bot.add_plugin(plugin)
