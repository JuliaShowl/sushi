import lightbulb
import random


plugin = lightbulb.Plugin('choose')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option('opt2', 'Second option', type=str, required=True)
@lightbulb.option('opt1', "First option", type=str, required=True)
@lightbulb.command('choose','Choose between two options', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def choose(ctx: lightbulb.Context, opt1: str, opt2: str):
    choice = random.sample([opt1,opt2],1)
    await ctx.respond(f"I choose **{choice[0]}**")

def load(bot):
    bot.add_plugin(plugin)
