import lightbulb
from miru import hikari
from miru.ext import nav
import requests

plugin = lightbulb.Plugin('images')

@plugin.command
@lightbulb.option('quantity', 'Number of photos to retreive (1-80) Default 15', type=int, required=False, min_value=1, max_value=80, default=15)
@lightbulb.option('query', "What do you want a photo of", type=str, required=True)
@lightbulb.command('pic','Get a photo', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def pic(ctx: lightbulb.Context, query: str, quantity: int):
    try:
        r = requests.get("https://api.qwant.com/v3/search/images",
        params={
            'count': quantity,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'offset': 0,
            'device': 'desktop'
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]
        
        buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
        navigator = nav.NavigatorView(pages=urls, buttons=buttons)
        await navigator.send(ctx.interaction)
    except:
        await ctx.respond("Unable to get images with that query.")

def load(bot):
    bot.add_plugin(plugin)
