from tokenize import String
import lightbulb
import math

plugin = lightbulb.Plugin('misc')
        
@plugin.command
@lightbulb.option('equation','Equation to solve', type=str)
@lightbulb.command('solve','quick mafs')
@lightbulb.implements(lightbulb.SlashCommand)
async def solve(ctx):
    if "life" in ctx.options.equation.lower():
        await ctx.respond("42")
        return
    try:
        eqn = eval(ctx.options.equation)
        resp = str(ctx.options.equation) + " = " + str(eqn)
        await ctx.respond(resp)
    except:
        await ctx.respond("Invalid equation.")
def load(bot):
    bot.add_plugin(plugin)
