from tokenize import String
import lightbulb
import random
import hikari

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SUSHI = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


plugin = lightbulb.Plugin('modify')
plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)

@plugin.command
@lightbulb.option("media","Media to be added", type=str, required=True)
@lightbulb.option("responder", "Responder to be added to", type=str, required=True, choices=["sushi", "egg", "souris_plant","munchie"])
@lightbulb.command("add", "Add media to database", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context, responder: str, media: str):
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [[media]]
        }
    except HttpError as err:
        print(err)

    if(responder == "sushi"):
        try:
            sheet.values().append(spreadsheetId=SUSHI, range="Sheet1!A:A", valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    elif(responder == "egg"):
        try:
            sheet.values().append(spreadsheetId=SUSHI, range="Sheet2!A:A", valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    elif(responder == "souris_plant"):
        try:
            sheet.values().append(spreadsheetId=SUSHI, range="Sheet3!A:A", valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    elif(responder == "munchie"):
        try:
            sheet.values().append(spreadsheetId=SUSHI, range="Sheet4!A:A", valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    else:
        await ctx.respond("Responder not recgonized")
        return

    await ctx.respond(f"Added {media} to `{responder}`!")

@plugin.command
@lightbulb.option("media","Media to be removed", type=str, required=True)
@lightbulb.command("remove", "Remove media from database", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def remove(ctx: lightbulb.Context, media: str):
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        value_range_body = {}
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet1!A:A").execute()
        values = result.get('values', [])

        for i in range(len(values)):
            if(values[i][0] == media):
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '0',
                                "dimension": "ROWS",
                                "startIndex": i,
                                "endIndex": i+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=SUSHI,body=request_body).execute()
                await ctx.respond(f"Removed {media} to from database!")
                return

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet2!A:A").execute()
        values = result.get('values', [])

        for i in range(len(values)):
            if(values[i][0] == media):
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '1802442433',
                                "dimension": "ROWS",
                                "startIndex": i,
                                "endIndex": i+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=SUSHI,body=request_body).execute()
                await ctx.respond(f"Removed {media} to from database!")
                return
        
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet3!A:A").execute()
        values = result.get('values', [])

        for i in range(len(values)):
            if(values[i][0] == media):
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '2057942648',
                                "dimension": "ROWS",
                                "startIndex": i,
                                "endIndex": i+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=SUSHI,body=request_body).execute()
                await ctx.respond(f"Removed {media} to from database!")
                return

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet4!A:A").execute()
        values = result.get('values', [])

        for i in range(len(values)):
            if(values[i][0] == media):
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '269933147',
                                "dimension": "ROWS",
                                "startIndex": i,
                                "endIndex": i+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=SUSHI,body=request_body).execute()
                await ctx.respond(f"Removed {media} from database!")
                return
    except HttpError as err:
        print(err)

    await ctx.respond(f"Unable to find media")

@plugin.command
@lightbulb.command("Add Sushi", "Add pictures to sushi", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_sushi(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "ROWS",
                'values': urls
        }
        sheet.values().append(spreadsheetId=SUSHI, range="Sheet1!A:A", valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    await ctx.respond(f"Added {media} to `sushi`.")

@plugin.command
@lightbulb.command("Add Egg", "Add pictures to Egg", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_egg(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "ROWS",
                'values': urls
        }
        sheet.values().append(spreadsheetId=SUSHI, range="Sheet2!A:A", valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    await ctx.respond(f"Added {media} to `egg`.")

@plugin.command
@lightbulb.command("Add Munchie", "Add pictures to sushi", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_munchie(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "ROWS",
                'values': urls
        }
        sheet.values().append(spreadsheetId=SUSHI, range="Sheet4!A:A", valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    await ctx.respond(f"Added {media} to `munchie`.")

def load(bot):
    bot.add_plugin(plugin)
