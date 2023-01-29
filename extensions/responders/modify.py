import lightbulb
import hikari
from . import remove_media

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
@lightbulb.option("responder", "Responder to be added to", type=str, required=True, choices=["sushi", "egg", "souris_plant","munchie", "bread"])
@lightbulb.command("add", "Add media to database", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context, responder: str, media: str):
    if "https://discord.com/channels/" in media:
        message_ids = media.split('/')
        message = await ctx.bot.rest.fetch_message(message_ids[-2],message_ids[-1])
        media = []
        for a in message.attachments:
            media.append(str(a.url))
    else:
        media = media.split(',')
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [media]
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
    elif(responder == "bread"):
        try:
            sheet.values().append(spreadsheetId=SUSHI, range="Sheet5!A:A", valueInputOption=value_input_option, body=value_range_body).execute()
        except HttpError as err:
            print(err)
    else:
        await ctx.respond("Responder not recgonized")
        return
    pics = "\n".join(str(x) for x in media) 
    await ctx.respond(f"Added {pics} to `{responder}`!")

@plugin.command
@lightbulb.option("media","Media to be removed", type=str, required=True)
@lightbulb.command("remove", "Remove media from database", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def remove(ctx: lightbulb.Context, media: str):
    try:
        await remove_media.remove_sushi(media)
        await remove_media.remove_egg(media)
        await remove_media.remove_plant(media)
        await remove_media.remove_munchie(media)
        await remove_media.remove_bread(media)
        await ctx.respond(f"Removed {media} from database!")
        return
    except:
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
