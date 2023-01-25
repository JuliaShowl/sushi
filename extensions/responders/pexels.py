import lightbulb
from miru import hikari
from miru.ext import nav
from pexels_api import API

plugin = lightbulb.Plugin('pexels')

@plugin.command
@lightbulb.option('quantity', 'Number of photos to retreive (1-80) Default 15', type=int, required=False, min_value=1, max_value=80, default=15)
@lightbulb.option('query', "What do you want a photo of", type=str, required=True)
@lightbulb.command('pic','Get a photo', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def meme(ctx: lightbulb.Context, query: str, quantity: int):
    PEXELS_API_KEY = ''
    api = API(PEXELS_API_KEY)

    api.search(query, page=1, results_per_page=quantity)

    photos = api.get_entries()
    pics = []
    for photo in photos:
        embed = hikari.Embed()
        embed.set_image(photo.original)
        embed.set_footer(f"Photographer: {photo.photographer}")
        pics.append(embed)
    
    buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
    navigator = nav.NavigatorView(pages=pics, buttons=buttons)
    await navigator.send(ctx.interaction)

def load(bot):
    bot.add_plugin(plugin)
