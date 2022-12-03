import lightbulb
import hikari
import random

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SUSHI = '' #Spreadhseet ID here
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '' #Google service account JSON here
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('Responders')

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
@lightbulb.command('zimzalabim','Are you ready for this?')
@lightbulb.implements(lightbulb.SlashCommand)
async def zimzalabim(ctx):
    f = hikari.File('./media/zimzalabim.mp4')
    await ctx.respond(f)

@plugin.command
@lightbulb.command('pantomime','Like a pantomime')
@lightbulb.implements(lightbulb.SlashCommand)
async def pantomime(ctx):
    f = hikari.File('./media/pantomime.mp4')
    await ctx.respond(f)


def load(bot):
    bot.add_plugin(plugin)
