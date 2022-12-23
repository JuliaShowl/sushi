import lightbulb
import hikari

plugin = lightbulb.Plugin('votehelp')
# Uncomment to limit
# plugin.add_checks(
#     lightbulb.has_roles(<roleID>,mode=any)
# )

@plugin.command
@lightbulb.command('votehelp','List voting commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def votehelp(ctx):
    va = "`/va <count|optional>` - Gets voting account info. Default 1, Min 1, Max 3.\n"
    votecount = "`/votecount` - Gets account totals.\n"
    reset = "`/reset` - Resets voting accounts.\n"
    resp = f"{va}{votecount}{reset}"
    embed = hikari.Embed(title="SushiBot Voting Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)