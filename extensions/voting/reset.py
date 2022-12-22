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

plugin = lightbulb.Plugin('reset')

@plugin.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command('reset','Resets voting sheets')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx):
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        requests = {
                'requests':[
                    {
                        "repeatCell":{
                            "cell":{
                                "userEnteredValue":{
                                    "stringValue":"Not Voted"
                                }
                            },
                            "range":{
                                "sheetId": '0',
                                "startRowIndex": 2,
                                "endRowIndex": 100,
                                "startColumnIndex": 3,
                                "endColumnIndex": 4
                            },
                            "fields":"userEnteredValue"
                        }
                    }
                ],
        }
        sheet.batchUpdate(spreadhSheetId=MNET_SHEET,body=requests).execute()

        await ctx.respond("Accounts reset!")
    except HttpError as err:
        print(err)


def load(bot):
    bot.add_plugin(plugin)
