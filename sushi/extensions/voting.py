import lightbulb
import hikari

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

MNET_SHEET = '' #Spreadsheet ID here
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '' #Google service account JSON here
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('Voting')

async def voteAccounts(user):
    username = ''
    password = ''
    rng = "Sheet1!C"
    rng2 = ":D"
    try: 
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=MNET_SHEET,
                                    range="Sheet1!A2:C").execute()
        values = result.get('values', [])
        for i in range(len(values)):
            if values[i][2] == "Not Voted":
                username = values[i][0]
                password = values[i][1]
                rng = rng + str(i+2)
                rng2 = rng2 + str(i+2)
                sheet.values().update(spreadsheetId=MNET_SHEET,range=(rng+rng2),valueInputOption='USER_ENTERED',body={'majorDimension':'COLUMNS','values':[["Done"],[user]]}).execute()
                return (username,password)
            if i == len(values) and values[i][2] == "Done":
                return None
    except HttpError as err:
        print(err)

@plugin.command
# @lightbulb.add_checks(lightbulb.has_roles(ADD ROLE IDs HERE,mode=any)) Uncomment and add role IDs to restrict
@lightbulb.add_cooldown(10.0,1,lightbulb.UserBucket)
@lightbulb.option('count','How many accounts to get', type=int, default=1, max_value=3)
@lightbulb.command('va','Get voting account info')
@lightbulb.implements(lightbulb.SlashCommand)
async def va(ctx):
    resp = ""
    user = ctx.author.username
    for i in range(ctx.options.count):
        task = (await voteAccounts(user))
        if task is None:
            await ctx.respond("All accounts have been used.")
            if resp:
                await ctx.respond(resp,flags=hikari.MessageFlag.EPHEMERAL,delete_after=5)
            else:
                return
        else:
            resp = resp + "Username:\n```"+task[0]+"```\nPassword:\n```"+task[1]+"```\n"
    await ctx.respond(resp,flags=hikari.MessageFlag.EPHEMERAL,delete_after=5)

@plugin.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command('votecount','Returns vote count info')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx):
    count = 0
    try: 
        service = build('sheets', 'v4', credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=MNET_SHEET,
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
