from tokenize import String
from datetime import datetime
import lightbulb
import hikari

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
@lightbulb.option("delete_message", "Delete the messages after the ban? (up to 7 days, leave empty or set to 0 to not delete)", type=int, min_value = 0, max_value = 7, default = 0 ,required=False)
@lightbulb.option("user", "User you want to ban", required=True)
@lightbulb.command("ban", "Ban a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context, user: hikari.Member, delete_message: int, reason: str):
    user_id = ctx.options.user.replace('<','').replace('>','').replace('@','')
    username = await ctx.bot.rest.fetch_user(user_id)
    delete = delete_message or 0
    await ctx.respond(f"Banning **{username}**")
    await ctx.bot.rest.ban_member(user = user_id, guild = ctx.get_guild(), reason = reason, delete_message_days=delete)
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        rng = 'Sheet1!A:A'

        # How the input data should be interpreted.
        value_input_option = 'USER_ENTERED'

        value_range_body = {
            "majorDimension": "COLUMNS",
           'values': [[str(dt)] ,["Ban"], [str(username)], [str(user_id)], [str(reason)], [str(ctx.author)]]
        }

        sheet.values().append(spreadsheetId=PUNISHMENTS, range=rng, valueInputOption=value_input_option, body=value_range_body).execute()

    except HttpError as err:
        print(err)

    await ctx.edit_last_response(f"{username} has been banned for `{reason}`")
    
@plugin.command()
@lightbulb.option("reason", "Reason for unban", type=str, required=False, default="Not specified")
@lightbulb.option("user", "the user you want to unban (Please use their user ID)", hikari.Snowflake, required=True)
@lightbulb.command("unban", "Unban a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context, user: hikari.Snowflake, reason: str):
    username = await ctx.bot.rest.fetch_user(user)
    await ctx.respond(f"Unbanning **{username}**")
    await ctx.bot.rest.unban_member(user = user, guild = ctx.get_guild(), reason = reason)
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
