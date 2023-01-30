import lightbulb

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SUSHI = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('remove_media')

async def remove_sushi(media):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

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
                return
    except HttpError as err:
        print(err)

async def remove_egg(media):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

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
                return
    except HttpError as err:
        print(err)

async def remove_plant(media):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

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
                return
    except HttpError as err:
        print(err)

async def remove_munchie(media):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

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
                return
    except HttpError as err:
        print(err)

async def remove_bread(media):
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SUSHI,
                                    range="Sheet5!A:A").execute()
        values = result.get('values', [])

        for i in range(len(values)):
            if(values[i][0] == media):
                request_body = {
                    "requests":[{
                            "deleteDimension": {
                                "range": {
                                "sheetId": '1201282877',
                                "dimension": "ROWS",
                                "startIndex": i,
                                "endIndex": i+1
                                }
                            }
                        }]
                }  
                sheet.batchUpdate(spreadsheetId=SUSHI,body=request_body).execute()
                return
    except HttpError as err:
        print(err)

def load(bot):
    bot.add_plugin(plugin)