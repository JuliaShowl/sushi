import lightbulb
import hikari
import requests

plugin = lightbulb.Plugin('bored')
@plugin.command
# @lightbulb.option("type", "Type of activity to choose", type=str, required=False, choices=["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])
@lightbulb.option("type", "Type of activity to choose", type=str, required=False, choices=["education", "recreational", "social", "charity", "cooking", "relaxation", "busywork"])
@lightbulb.command("bored", "Get a random activity.", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def request(ctx: lightbulb.Context, type: str):
    # if type:
    #     request = requests.get(f"http://www.boredapi.com/api/activity?type={type}")
    # else:
    #     request = requests.get("http://www.boredapi.com/api/activity")

    if type:
        request = requests.get(f"https://bored-api.appbrewery.com/filter?type={type}")
    else:
        request = requests.get("https://bored-api.appbrewery.com/random")
    
    re = request.json()
    await ctx.respond(re['activity'])


def load(bot):
    bot.add_plugin(plugin)