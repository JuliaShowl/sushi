from tokenize import String
from datetime import datetime
import lightbulb
import hikari
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

PUNISHMENTS = ''
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('ban')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.guild_only
)

@plugin.command()
@lightbulb.option("reason", "Reason for banning member", type=str, required=False, default="Not specified")
@lightbulb.option("delete_message", "Delete the messages after the ban? (time in seconds between 0 and 604800 (7 days))", type=int, min_value = 0, max_value = 7, default = 0 ,required=False)
@lightbulb.option("user", "User you want to ban", type=hikari.User,required=True)
@lightbulb.command("ban", "Ban a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context, user: hikari.User, delete_message: int, reason: str):
    try:
        delete = delete_message or 0
        await ctx.respond(f"Banning **{user}**")
        await ctx.bot.rest.ban_member(user = user.id, guild = ctx.get_guild(), reason = reason, delete_message_seconds=delete)
        dt = datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        try:
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()
            rng = 'Sheet1!A:A'

            # How the input data should be interpreted.
            value_input_option = 'USER_ENTERED'

            value_range_body = {
                "majorDimension": "COLUMNS",
            'values': [[str(dt)] ,["Ban"], [str(user)], [str(user.id)], [str(reason)], [str(ctx.author)]]
            }

            sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

        except HttpError as err:
            print(err)

        await ctx.edit_last_response(f"{user} has been banned for `{reason}`")
    except:
        await ctx.respond("Unable to ban that user. That user may be higher than the bot.")
    
@plugin.command()
@lightbulb.option("reason", "Reason for unban", type=str, required=False, default="Not specified")
@lightbulb.option("user", "the user you want to unban (Please use their user ID)", type=hikari.Snowflake, required=True)
@lightbulb.command("unban", "Unban a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context, user: hikari.Snowflake, reason: str):
    try:
        username = await ctx.bot.rest.fetch_user(user)
        await ctx.respond(f"Unbanning **{username}**")
        await ctx.bot.rest.unban_member(user = user, guild = ctx.get_guild(), reason = reason)
        dt = datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        try:
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()
            rng = 'Sheet1!A:A'

            # How the input data should be interpreted.
            value_input_option = 'USER_ENTERED'

            value_range_body = {
                "majorDimension": "COLUMNS",
            'values': [[str(dt)] ,["Unban"], [str(username)], [str(user)], [str(reason)], [str(ctx.author)]]
            }

            sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

        except HttpError as err:
            print(err)

        await ctx.edit_last_response(f"{username} has been unbanned for `{reason}`!")
    except:
        await ctx.respond("Unable to unban that user. Please make sure you use their UserID and check if they are banned or not.")
    
@plugin.command()
@lightbulb.command("banlist", "List of users banned from server")
@lightbulb.implements(lightbulb.SlashCommand)
async def banlist(ctx: lightbulb.Context):
    bans = await ctx.bot.rest.fetch_bans(ctx.get_guild())
    response = ''
    if not bans:
        response = "No one is banned from this server."
    else:
        for i, users in enumerate(bans, start=1):
            response += f"**{i}. {users.user}** - {users.reason or 'Not specified'}\n"
    embed = hikari.Embed(title="List of Banned Members", description=response, color='0000FF')
    embed.set_footer(f"{len(bans)} Members in total.")
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(plugin)
