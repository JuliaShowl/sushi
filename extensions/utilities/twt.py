import requests
import lightbulb

plugin = lightbulb.Plugin("twt")

plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option("tweet", "Tweet to get images from.", type=str, required=True)
@lightbulb.command("twt", "Get images from a tweet", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def twt(ctx: lightbulb.context, tweet: str):
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
                await ctx.respond(pics)
            else:
                await ctx.respond("Unable to get media from that tweet.")
        except:
            await ctx.respond("Unable to get media from that tweet.")
    else:
        await ctx.respond("Not a vaild tweet.")


def load(bot):
    bot.add_plugin(plugin)