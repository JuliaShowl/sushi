import requests
import lightbulb
import re
import hikari

plugin = lightbulb.Plugin("twt")

plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option("text", "Include the text from the tweet?", type=bool, required=False, default=False, choices=[True,False])
@lightbulb.option("tweet", "Tweet to get images from.", type=str, required=True)
@lightbulb.command("twt", "Get images from a tweet", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def twt(ctx: lightbulb.context, tweet: str, text: bool):
    if "twitter.com" in tweet or "x.com" in tweet:
        try:
            tweet_id = tweet.split('/')
            tweet_id = tweet_id[-1]
            tweet_id = tweet_id.split('?')
            tweet_id = tweet_id[0]
            response = requests.get(f'https://api.vxtwitter.com/Twitter/status/{tweet_id}')
            media = response.json().get('mediaURLs')
            if media:
                pics = "\n".join(str(x) for x in media) 
                if text:
                    txt = response.json().get('text')
                    if txt:
                        txt = re.sub(r'https://t.co\S+', '', txt)
                        dsp = response.json().get('user_name')
                        url = response.json().get('tweetURL')
                        embed = hikari.Embed(title=f'{dsp} on Twitter', description=txt, color='00ACEE', url=url)
                        await ctx.respond(embed=embed)
                        await ctx.get_channel().send(pics)
                    else:
                        await ctx.respond(pics)
                else:
                    await ctx.respond(pics)
            else:
                await ctx.respond("Unable to get media from that tweet.")
        except:
            await ctx.respond("Unable to get media from that tweet.")
    else:
        await ctx.respond("Not a vaild tweet.")


def load(bot):
    bot.add_plugin(plugin)