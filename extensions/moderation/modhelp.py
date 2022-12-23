import lightbulb
import hikari

plugin = lightbulb.Plugin('modhelp')
plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)

@plugin.command
@lightbulb.command('modhelp','List moderation commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def modhelp(ctx):
    warnings = "`/warn <@user> <reason|optional>` - Internal warning for user\n`/clearwarnings <@user>` - Removes all warnings from user\n"
    timeout = "`/timeout <@user> <reason|optional> <days|optional> <hours|optional> <minutes|optional> <seconds|optional>` - Times out user for given duration. If no duration is specified, will attempt to remove timeout from user\n"
    kick = "`/kick <@user> <reason|optional>` - Kicks user\n"
    bans = "`/ban <@user> <reason|optional>` - Bans user\n`/unban <userID> <reason|optional>` - Unbans user\n`/banlist` - Lists all mebmers banned from server\n"
    history = "`/history <@user>` - Gets punishment history for user. `Timestamp local to copmuter running bot - Type - Reason - Duration - Punisher`\n"
    resp = f"**Warnings**\n{warnings}\n**Timeout**\n{timeout}\n**Kick**\n{kick}\n**Bans**\n{bans}\n**History**\n{history}\n"
    embed = hikari.Embed(title="SushiBot Moderation Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
