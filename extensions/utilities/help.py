import lightbulb
import hikari

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help','List commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    sushi = "`/sushi` - Returns a picture of Sushi, Mia's hamster\n"
    egg = "`/egg` - Returns a picture of Egg, Souris' cat\n"
    plant = "`/souris_plant` - Returns a picture of Souris' bonsai or some random Reddit plant\n"
    zim = "`/zimzalabim` - Are you ready for this?\n"
    pan = "`/pantomime` - Like a pantomime\n"
    math = "`/solve <equation>` - Solves equations. Supports python's math library\n"
    yoink = "`/yoihnk <emote>` - Grabs custom emote\n"
    resp = f"{sushi}{egg}{plant}{zim}{pan}{math}{yoink}"
    embed = hikari.Embed(title="SushiBot Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
