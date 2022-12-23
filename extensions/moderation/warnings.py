from tokenize import String
from datetime import datetime
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

plugin = lightbulb.Plugin('warnings')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)

@plugin.command
@lightbulb.option('user','The user to warn')
@lightbulb.option('reason','Reason for warning',type=str,required=False,default='Not specified')
@lightbulb.command('warn','Warn a user for breaking a rule', auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def warn(ctx: lightbulb.Context, user: hikari.Member, reason: str):
    user_id = ctx.options.user.replace('<','').replace('>','').replace('@','')
    username = await ctx.bot.rest.fetch_user(user_id)

    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        rng = 'Sheet1!A:A'

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'

        value_range_body = {
            "majorDimension": "COLUMNS",
           'values': [[str(dt)] ,["Warning"], [str(username)], [str(user_id)], [str(reason)], [str(ctx.author)]]
        }

        sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    resp = f"{username} has been warned for `{reason}`"
    await ctx.respond(resp)

@plugin.command
@lightbulb.option('user','User to remove warnings from')
@lightbulb.command('clearwarnings','Remove all warnings from user')
@lightbulb.implements(lightbulb.SlashCommand)
async def clearwarnings(ctx: lightbulb.Context, user: hikari.Member):
    user_id = ctx.options.user.replace('<','').replace('>','').replace('@','')
    username = await ctx.bot.rest.fetch_user(user_id)

    try:
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=PUNISHMENTS,
                                    range="Sheet1!A2:E").execute()
        values = result.get('values', [])
        for i in range(len(values)-1,-1,-1):
            if values[i][3] == user_id and values[i][1] == 'Warning':
                rng = i + 1
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '0',
                                "dimension": "ROWS",
                                "startIndex": rng,
                                "endIndex": rng+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=PUNISHMENTS,body=request_body).execute()

    except HttpError as err:
        print(err)
    
    resp = f"All warnings for {username} have been removed."
    await ctx.respond(resp)

def load(bot):
    bot.add_plugin(plugin)
