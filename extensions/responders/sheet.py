from tokenize import String
import lightbulb
import random

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SUSHI = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('sheet')

@plugin.command
@lightbulb.command('sushi','Returns a picture of sushi')
@lightbulb.implements(lightbulb.SlashCommand)
async def sushi(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet1!A:A").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)

@plugin.command
@lightbulb.command('egg','Returns a picture of egg')
@lightbulb.implements(lightbulb.SlashCommand)
async def egg(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet1!B:B").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)
    
@plugin.command
@lightbulb.command('souris_plant','Returns a picture of souris\' plant')
@lightbulb.implements(lightbulb.SlashCommand)
async def souris_plant(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet1!C:C").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)

@plugin.command
# @lightbulb.add_checks(lightbulb.has_roles(<roleID>,mode=any)) Uncomment to limit
@lightbulb.option("image","Image to be added", type=str, required=True)
@lightbulb.option("responder", "Responder to be added to", type=str, required=True, choices=["sushi", "egg", "souris_plant"])
@lightbulb.command("add", "Add picture to responder", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context, responder: str, image: str):
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'
    except HttpError as err:
        print(err)

    if(responder == "sushi"):
        try:
            rng = 'Sheet1!A:A'
            value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [[image]]
            }

            sheet.values().append(spreadsheetId=SUSHI, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    elif(responder == "egg"):
        try:
            rng = 'Sheet1!B:B'
            value_range_body = {
                "majorDimension": "COLUMNS",
            'values': [[image]]
            }

            sheet.values().append(spreadsheetId=SUSHI, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    elif(responder == "souris_plant"):
        try:
            rng = 'Sheet1!C:C'
            value_range_body = {
                "majorDimension": "COLUMNS",
            'values': [[image]]
            }

            sheet.values().append(spreadsheetId=SUSHI, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    else:
        await ctx.respond("Responder not recgonized")
        return

    await ctx.respond("Added to bot!")

def load(bot):
    bot.add_plugin(plugin)
