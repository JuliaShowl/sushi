from tokenize import String
import lightbulb
import math
import requests

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

@plugin.command
@lightbulb.command('dadjoke', "Get a random dad joke", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dadjoke(ctx: lightbulb.Context):
    header = {"Accept": "text/plain"}
    response = requests.get('https://icanhazdadjoke.com/', headers=header)
    await ctx.respond(response.text)

def load(bot):
    bot.add_plugin(plugin)
