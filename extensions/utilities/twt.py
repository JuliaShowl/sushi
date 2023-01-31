import lightbulb
import tweepy

plugin = lightbulb.Plugin("twt")

plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option("tweet", "Tweet to get images from.", type=str, required=True)
@lightbulb.command("twt", "Get images from a tweet", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def twt(ctx: lightbulb.context, tweet: str):
    client = tweepy.Client("Bearer Access Token")
    if "twitter.com" not in tweet:
        await ctx.respond("Not a vaild tweet.")
        return
    else:
        try:
            media = []
            tweet_id = tweet.split('/')
            tweet_id = tweet_id[-1]
            tweet_id = tweet_id.split('?')
            tweet_id = tweet_id[0]
            response = client.get_tweet(tweet_id, media_fields=['url','variants'],expansions=['attachments.media_keys'])
            urls = response.includes["media"]
            for u in urls:
                if u["url"] is not None:
                    media.append(u["url"])
                if u["variants"] is not None:
                    for i in u["variants"]:
                        if ".mp4" in i["url"]:
                            media.append(i["url"])
                            break
            pics = "\n".join(str(x) for x in media) 
            await ctx.respond(pics)
        except:
            await ctx.respond("Unable to get media from that tweet.")

def load(bot):
    bot.add_plugin(plugin)