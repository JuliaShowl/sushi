from tokenize import String
import lightbulb
import requests

plugin = lightbulb.Plugin('meme')

@plugin.command
@lightbulb.command('meme','Get a random meme')
@lightbulb.implements(lightbulb.SlashCommand)
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    meme = response.json()
    while meme["nsfw"]:
        response = requests.get('https://meme-api.com/gimme')
        meme = response.json()
    await ctx.respond(meme["url"])

def load(bot):
    bot.add_plugin(plugin)
