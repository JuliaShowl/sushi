import lightbulb
import hikari

plugin = lightbulb.Plugin('votehelp')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.command('votehelp','List voting commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def votehelp(ctx):
    va = "`/va <count|optional>` - Gets voting account info.\n"
    ga = "`/ga` - Generates account information for sign up.\n"
    votecount = "`/votecount` - Gets account totals.\n"
    reset = "`/reset` - Resets voting accounts. *Limited to bot owner*\n"
    resp = f"{va}{ga}{votecount}{reset}"
    embed = hikari.Embed(title="SushiBot Voting Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)