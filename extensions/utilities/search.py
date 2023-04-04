import lightbulb
import hikari
from miru.ext import nav
import requests

plugin = lightbulb.Plugin('search')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option('query', "What are you looking for?", type=str, required=True)
@lightbulb.command('search','Search the web.', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def search(ctx: lightbulb.Context, query: str):
    try:
        r = requests.get("https://api.qwant.com/v3/search/web",
        params={
            'count': 10,
            'q': query,
            'safesearch': 1,
            'locale': 'en_US',
            'offset': 0,
            'device': 'desktop'
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        })

        response = r.json().get('data').get('result').get('items')
        results = []
        reply = []
        response = response["mainline"]
        for r in response:
            if "ads" not in r["type"]:
                results.append(r)
        for result in results:
            for r in result['items']:
                if r.get('title') is not None:
                    if r.get('desc') is not None:
                        embed = hikari.Embed(title=r['title'], description=f"{r['desc']}\n\n[Link]({r['url']})")
                    else:
                        embed = hikari.Embed(title=r['title'], description=f"[Link]({r['url']})")
                    if r.get('media') is not None:
                        embed.set_image(r['media'][0]['pict']['url'])
                    if r.get('thumbnail') is not None:
                        embed.set_image(r['thumbnail'])
                    reply.append(embed)

        buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
        navigator = nav.NavigatorView(pages=reply, buttons=buttons)
        await navigator.send(ctx.interaction)

    except:
        await ctx.respond("Unable to query that result.")

def load(bot):
    bot.add_plugin(plugin)
