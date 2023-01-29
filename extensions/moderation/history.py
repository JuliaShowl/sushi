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
@lightbulb.option('user','User to get punishments for',type=hikari.User)
@lightbulb.command('history','See all user\'s punishments', auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def history(ctx: lightbulb.Context, user: hikari.User):
    resp = []
    response = ''
    title = "Punishments for " + str(user)
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=PUNISHMENTS,
                                    range="Sheet1!A2:G").execute()
        values = result.get('values', [])
        for i in range(len(values)):
            if values[i][3] == str(user.id):
                resp.append(values[i])

    except HttpError as err:
        print(err)

    if not resp:
        response = str(user) + " has not been punished."
    else:
        for i in range(len(resp)):
            if(len(resp[i]) == 7):
                response += resp[i][0] +" - "+ resp[i][1] +" - "+ resp[i][4] +" - "+ resp[i][6] +" - "+ resp[i][5] + "\n"
            else:
                response += resp[i][0] +" - "+ resp[i][1] +" - "+ resp[i][4] +" - "+ resp[i][5] + "\n"
                

    embed = hikari.Embed(title=title,description=response, color='FF0000')
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(plugin)
