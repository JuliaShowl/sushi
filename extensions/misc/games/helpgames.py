import lightbulb
import hikari

plugin = lightbulb.Plugin('helpgames')

@plugin.command
@lightbulb.command('helpgames','List game commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    fq = "`/fq <count|optional> <options|optional>` - Guess the flag\n"
    cq = "`/cq <count|optional> <options|optional>` - Guess the capital\n"
    trivia = "`/trivia <count|optional> <category|optional> <difficulty|optional>` - Get trivia questions\n"
    vs = "`/vs <type> <count|optional> <category|optional> <difficulty|optional> <options|optional> - Play the quizzes against friends.\n"
    rps = "`/rps <players|optional> <user|optional> - Play rock, paper, scissors against Sushi or a friend!\n"
    resp = f"**Games**\n{fq}{cq}{trivia}{vs}{rps}"
    embed = hikari.Embed(title="SushiBot Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
