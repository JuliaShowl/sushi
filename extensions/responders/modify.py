from time import sleep
import lightbulb
import hikari
import requests

from supabase import create_client

url = ""
key = ""
supabase = create_client(url, key)

file_types = [".jpg" , ".jpeg" , ".JPG" , ".JPEG" , ".png" , ".PNG" , ".gif" , ".gifv" , ".webm" , ".mp4" , ".wav" , ".mp3" , ".mp4" , "https://tenor.com", "https://giphy.com", "https://gfycat.com/", "https://url.misobot.xyz/", "https://www.youtube.com/", "https://youtu.be/"]

plugin = lightbulb.Plugin('modify')

@plugin.command
@lightbulb.option("embed","Embed images?", type=bool, required=False, default=True)
@lightbulb.option("media","Media to be added", type=str, required=True)
@lightbulb.option("responder", "Responder to be added to", type=str, required=True, choices=["sushi", "egg", "plant","munchie", "bread"])
@lightbulb.command("add", "Add media to database", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context, responder: str, media: str, embed: bool):
    pets = ['sushi', 'egg', 'munchie']
    misc = ['plant', 'bread']
    media = media.split(',')
    content = []
    non = []
    for med in media:
        if "https://discord.com/channels/" in med:
            source = med
            message_ids = med.split('/')
            message = await ctx.bot.rest.fetch_message(message_ids[-2],message_ids[-1])
            if any([x in str(message.content) for x in file_types]):
                if any([x in responder for x in pets]):
                    try:
                        supabase.table("pets").insert({'url': str(a.ur), 'type': responder, 'source':source}).execute()
                        content.append(str(message.content))
                    except Exception as e:
                        non.append(e)
                elif any([x in responder for x in misc]):
                    try:
                        supabase.table("misc").insert({'url': str(message.content), 'type': responder, 'source':source}).execute()
                        content.append(str(message.content))
                    except Exception as e:
                        non.append(e)
            elif message.attachments is not None:
                for a in message.attachments:
                    if any([x in responder for x in pets]):
                        try:
                            supabase.table("pets").insert({'url': str(a.url), 'type': responder, 'source':source}).execute()
                            content.append(str(a.url))
                        except Exception as e:
                            non.append(e)
                    elif any([x in responder for x in misc]):
                        try:
                            supabase.table("misc").insert({'url': str(a.url), 'type': responder, 'source':source}).execute()
                            content.append(str(a.url))
                        except Exception as e:
                            non.append(e)
        if "twitter.com" in med or "x.com" in med:
            try:
                source = med
                tweet_id = med.split('/')
                tweet_id = tweet_id[-1]
                tweet_id = tweet_id.split('?')
                tweet_id = tweet_id[0]
                response = requests.get(f'https://api.vxtwitter.com/Twitter/status/{tweet_id}')
                med = response.json().get('mediaURLs')
                for m in med:
                    if any([x in responder for x in pets]):
                        try:
                            supabase.table("pets").insert({'url': str(m), 'type': responder, 'source':source}).execute()
                            content.append(str(m))
                        except Exception as e:
                            non.append(e)
                    elif any([x in responder for x in misc]):
                        try:
                            supabase.table("misc").insert({'url': str(m), 'type': responder, 'source':source}).execute()
                            content.append(str(m))
                        except Exception as e:
                            non.append(e)
            except Exception as e:
                non.append(e)
        if any([x in med for x in file_types]):
            if any([x in responder for x in pets]):
                try:
                    supabase.table("pets").insert({'url': str(med), 'type': responder, 'source':source}).execute()
                    content.append(str(med))
                except Exception as e:
                    non.append(e)
            elif any([x in responder for x in misc]):
                try:
                    supabase.table("misc").insert({'url': str(med), 'type': responder, 'source':source}).execute()
                    content.append(str(med))
                except Exception as e:
                    non.append(e)
        if len(non) > 0 and not content:
            await ctx.respond(non[0])
            for n in range(1,len(non)):
                await ctx.get_channel().send(non[n])
            return
        elif not content:
            await ctx.respond("Unable to find useable media.")
            return
    if embed:
        pics = "\n".join(str(x) for x in content)
    else:
        pics = ">\n".join(str("<" + x) for x in content)
        pics = pics + ">"
    if len(pics) < 1950:
        await ctx.respond(f"Added `{len(content)}` entries\n{pics} to `{responder}`!")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)
    else:
        await ctx.respond(f"Added `{len(content)}` entries to `{responder}`!")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)


@plugin.command
@lightbulb.option("media","Media to be removed", type=str, required=True)
@lightbulb.command("remove", "Remove media from database", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def remove(ctx: lightbulb.Context, media: str):
    try:
        supabase.table('pets').delete().eq('url', media).execute()
        supabase.table('misc').delete().eq('url', media).execute()
        await ctx.respond(f"Removed {media} from database!")
    except Exception as e:
        await ctx.respond(e)

@plugin.command
@lightbulb.command("Add Sushi", "Add pictures to sushi", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_sushi(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    non = []
    for i in target.attachments:
        try:
            supabase.table("pets").insert({'url': str(i.url), 'type': 'sushi', 'source':i.url}).execute()
            urls.append([str(i.url)])
            media += i.url + "\n"
        except Exception as e:
            non.append(e)

    if len(non) > 0 and not urls:
        await ctx.respond(non[0])
        for n in range(1,len(non)):
            await ctx.get_channel().send(non[n])
        return
    if len(media) < 1950:
        await ctx.respond(f"Added `{len(urls)}` entries\n{media} to `sushi`.")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)
    else:
        await ctx.respond(f"Added `{len(urls)}` entries to `sushi`.")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)

@plugin.command
@lightbulb.command("Add Egg", "Add pictures to Egg", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def add_egg(ctx: lightbulb.Context, target: hikari.Message):
    media = ""
    urls = []
    non = []
    for i in target.attachments:
        try:
            supabase.table("pets").insert({'url': str(i.url), 'type': 'egg', 'source':i.url}).execute()
            urls.append([str(i.url)])
            media += i.url + "\n"
        except Exception as e:
            non.append(e)

    if len(non) > 0 and not urls:
        await ctx.respond(non[0])
        for n in range(1,len(non)):
            await ctx.get_channel().send(non[n])
        return
    if len(media) < 1950:
        await ctx.respond(f"Added `{len(urls)}` entries\n{media} to `egg`.")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)
    else:
        await ctx.respond(f"Added `{len(urls)}` entries to `egg`.")
        if len(non) > 0:
            for n in non:
                await ctx.get_channel().send(n)

def load(bot):
    bot.add_plugin(plugin)
