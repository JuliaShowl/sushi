import lightbulb
import hikari

plugin = lightbulb.Plugin('helpgames')

@plugin.command
@lightbulb.command('helpgames','List game commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    fq = "`/fq <count|optional> <options|optional>` - Guess the flag\n"
    resp = f"**Games**\n{fq}"
    embed = hikari.Embed(title="SushiBot Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
