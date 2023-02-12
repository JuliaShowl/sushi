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

plugin = lightbulb.Plugin('sheet')

@plugin.command
@lightbulb.command('sushi','Returns a picture of sushi')
@lightbulb.implements(lightbulb.SlashCommand)
async def sushi(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
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
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet2!A:A").execute()
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
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet3!A:A").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)

@plugin.command
@lightbulb.command('munchie','Returns a picture of Munchie')
@lightbulb.implements(lightbulb.SlashCommand)
async def munchie(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet4!A:A").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)

@plugin.command
@lightbulb.command('bread','Returns a bread')
@lightbulb.implements(lightbulb.SlashCommand)
async def bread(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet5!A:A").execute()
        values = result.get('values', [])
        i = random.randrange(0,len(values))
        await ctx.respond(values[i][0])
    except HttpError as err:
        print(err)

@plugin.command
@lightbulb.command('responders', 'Gets all responders and their total entries.', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def responders(ctx: lightbulb.Context):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet1!A:A").execute()
        sushi = len(result.get('values', []))

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet2!A:A").execute()
        egg = len(result.get('values', []))

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet3!A:A").execute()
        plant = len(result.get('values', []))

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet4!A:A").execute()
        munchie = len(result.get('values', []))

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet5!A:A").execute()
        bread = len(result.get('values', []))


        resp_pets = f"Sushi - `{sushi}` entries\nEgg - `{egg}` entries\nMunchie - `{munchie}` entries\n"
        resp_misc = f"Souris_Plant - `{plant}` entries\nBread - `{bread}` entries\n"

        embed = hikari.Embed(title="Sushi Responders")
        embed.add_field("Pets", value=resp_pets)
        embed.add_field("Misc", value=resp_misc)
        await ctx.respond(embed=embed)
        
    except HttpError as err:
        print(err)


def load(bot):
    bot.add_plugin(plugin)
