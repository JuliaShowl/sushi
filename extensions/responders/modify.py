from time import sleep
import lightbulb
import hikari
from . import remove_media
import requests

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SUSHI = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

file_types = [".jpg" , ".jpeg" , ".JPG" , ".JPEG" , ".png" , ".PNG" , ".gif" , ".gifv" , ".webm" , ".mp4" , ".wav" , ".mp3" , ".mp4" , "https://tenor.com", "https://giphy.com"]

plugin = lightbulb.Plugin('modify')
@plugin.command
@lightbulb.option("embed","Embed images?", type=bool, required=False, default=True)
@lightbulb.option("media","Media to be added", type=str, required=True)
@lightbulb.option("responder", "Responder to be added to", type=str, required=True, choices=["sushi", "egg", "souris_plant","munchie", "bread"])
@lightbulb.command("add", "Add media to database", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context, responder: str, media: str, embed: bool):
    media = media.split(',')
    content = []
    for med in media:
        if "https://discord.com/channels/" in med:
            message_ids = med.split('/')
            message = await ctx.bot.rest.fetch_message(message_ids[-2],message_ids[-1])
            if "https://tenor.com" in str(message.content) or "https://giphy.com" in str(message.content):
                    content.append(str(message.content))
            elif message.attachments is not None:
                for a in message.attachments:
                    content.append(str(a.url))
        if "twitter.com" in med or "x.com" in med:
            try:
                tweet_id = med.split('/')
                tweet_id = tweet_id[-1]
                tweet_id = tweet_id.split('?')
                tweet_id = tweet_id[0]
                response = requests.get(f'https://api.vxtwitter.com/Twitter/status/{tweet_id}')
                med = response.json().get('mediaURLs')
                for m in med:
                    content.append(m)
            except:
                pass
        if any([x in med for x in file_types]):
            content.append(med)
        if not content:
            await ctx.respond("Unable to find useable media.")
            return
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'
        value_range_body = {
                "majorDimension": "COLUMNS",
                'values': [content]
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
    if embed:
        pics = "\n".join(str(x) for x in content)
    else:
        pics = ">\n".join(str("<" + x) for x in content)
        pics = pics + ">"
    if len(pics) < 1950:
        await ctx.respond(f"Added `{len(content)}` entries\n{pics} to `{responder}`!")
    else:
        await ctx.respond(f"Added `{len(content)}` entries to `{responder}`!")


@plugin.command
@lightbulb.option("media","Media to be removed", type=str, required=True)
@lightbulb.command("remove", "Remove media from database", pass_options=True, auto_defer=True)
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
@lightbulb.command("Add Sushi", "Add pictures to sushi", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_sushi(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

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

    if len(media) < 1950:
        await ctx.respond(f"Added `{len(urls)}` entries\n{media} to `sushi`.")
    else:
        await ctx.respond(f"Added `{len(urls)}` entries to `sushi`.")

@plugin.command
@lightbulb.command("Add Egg", "Add pictures to Egg", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_egg(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

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

    if len(media) < 1950:
        await ctx.respond(f"Added `{len(urls)}` entries\n{media} to `egg`.")
    else:
        await ctx.respond(f"Added `{len(urls)}` entries to `egg`.")

@plugin.command
@lightbulb.command("Add Munchie", "Add pictures to sushi", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_munchie(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    for i in target.attachments:
        urls.append([str(i.url)])
        media += i.url + "\n"
    try:
        service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

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

    if len(media) < 1950:
        await ctx.respond(f"Added `{len(urls)}` entries\n{media} to `munchie`.")
    else:
        await ctx.respond(f"Added `{len(urls)}` entries to `munchie`.")

def load(bot):
    bot.add_plugin(plugin)
