import lightbulb
import hikari
import random
import requests
import string
import re
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# The ID of a sample spreadsheet.
SHEET = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('votecount')

@plugin.command
# @lightbulb.add_checks(lightbulb.has_roles(<roleID>,mode=any)) Uncomment to limit
@lightbulb.command('votecount','Returns vote count info')
@lightbulb.implements(lightbulb.SlashCommand)
async def votecount(ctx):
    count = 0
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SHEET,
                                    range="Sheet1!C2:C").execute()
        values = result.get('values', [])
        for i in range(len(values)):
            if values[i][0] == "Done" or values[i][0] == "In Progress":
                count+=1
        await ctx.respond("Vote count\nVoted: `"+str(count)+"`\nNot voted: `"+str((len(values))-count)+"`\nTotal: `"+str(len(values))+"`")
    except HttpError as err:
        print(err)

def load(bot):
    bot.add_plugin(plugin)
