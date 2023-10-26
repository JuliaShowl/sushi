import lightbulb
import requests

plugin = lightbulb.Plugin('meme')

@plugin.command
@lightbulb.option('sub', "Get a meme from a specific subreddit", type=str, required=False)
@lightbulb.command('meme','Get a random meme', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def meme(ctx: lightbulb.Context, sub: str):
    if sub is not None:
        try:
            response = requests.get(f'https://meme-api.com/gimme/{sub}')
            meme = response.json()
            if meme["nsfw"]:
                await ctx.respond("Sorry that subreddit is marked as NSFW")
                return
            await ctx.respond(meme["url"])
        except:
            await ctx.respond("Invalid subreddit")
    else:
        response = requests.get(f'https://meme-api.com/gimme/')
        meme = response.json()
        if meme["nsfw"]:
            await ctx.respond("Sorry that subreddit is marked as NSFW")
            return
        await ctx.respond(meme["url"])
def load(bot):
    bot.add_plugin(plugin)
