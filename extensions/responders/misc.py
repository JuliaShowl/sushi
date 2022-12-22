from tokenize import String
import lightbulb
import hikari
import random
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
    eqn = eval(ctx.options.equation)
    resp = str(ctx.options.equation) + " = " + str(eqn)
    await ctx.respond(resp)

def load(bot):
    bot.add_plugin(plugin)
