import requests
import lightbulb
import random
import math
import hikari

plugin = lightbulb.Plugin('misc')
plugin.add_checks(
    lightbulb.guild_only
)
        
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

@plugin.command
@lightbulb.command('grr', "Eu")
@lightbulb.implements(lightbulb.SlashCommand)
async def grr(ctx: lightbulb.Context):
    await ctx.respond("😭🥺💧Eu💧💧E E😭😭 E EUE🥺🥺😭UUUUE😭🥺💧🥺😭 ue 💧ee😭🥺💧ue 🥺e e e😭. e 💧🥺😭Uueuuue.💧 😭🥺ee e🥺🥺😭eUEE 💧🥺💧EEE 💧💧😭U E 🥺😭EE H💧🥺😭E EUU💧🥺💧😭EUEH🥺😭💧💧ue e😭😭eeeeee💧💧💧uu🥺😭 hh")

@plugin.listener(hikari.GuildMessageCreateEvent)
async def cry(event):
    try:
        if 'grr' in event.content:
            if random.random() < .1:
                await plugin.bot.rest.create_message(event.channel_id, "😭🥺💧Eu💧💧E E😭😭 E EUE🥺🥺😭UUUUE😭🥺💧🥺😭 ue 💧ee😭🥺💧ue 🥺e e e😭. e 💧🥺😭Uueuuue.💧 😭🥺ee e🥺🥺😭eUEE 💧🥺💧EEE 💧💧😭U E 🥺😭EE H💧🥺😭E EUU💧🥺💧😭EUEH🥺😭💧💧ue e😭😭eeeeee💧💧💧uu🥺😭 hh")
    except:
        pass


def load(bot):
    bot.add_plugin(plugin)
