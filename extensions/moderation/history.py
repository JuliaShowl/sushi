from tokenize import String
from datetime import datetime, timedelta
import lightbulb
import hikari

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


PUNISHMENTS = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('history')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)

@plugin.command
@lightbulb.option('user','User to get punishments for')
@lightbulb.command('history','See all user\'s punishments')
@lightbulb.implements(lightbulb.SlashCommand)
async def history(ctx):
    user_id = ctx.options.user.replace('<','').replace('>','').replace('@','')
    resp = []
    response = ''
    username = await ctx.bot.rest.fetch_user(user_id)
    title = "Punishments for " + str(username)
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=PUNISHMENTS,
                                    range="Sheet1!A2:E").execute()
        values = result.get('values', [])
        for i in range(len(values)):
            if values[i][3] == user_id:
                resp.append(values[i])

    except HttpError as err:
        print(err)

    if not resp:
        response = str(username) + " has not been punished."
    else:
        for i in range(len(resp)):
            response += resp[i][0] +" - "+ resp[i][1] +" - "+ resp[i][4] + "\n"

    embed = hikari.Embed(title=title,description=response, color='FF0000')
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(plugin)
