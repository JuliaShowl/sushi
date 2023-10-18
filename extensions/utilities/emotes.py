import hikari
import lightbulb
import re

plugin = lightbulb.Plugin("emotes")
plugin.add_checks(
    lightbulb.guild_only
)

static_re = re.compile(r"<:([^:]+):(\d+)>")
animated_re = re.compile(r"<a:([^:]+):(\d+)>")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("emotes", "Emotes to yoink", required=True)
@lightbulb.command("yoink", "Steal emotes or sticker from a message.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def yoink(ctx: lightbulb.Context, emotes: hikari.Message):
    static = ""
    animated = ""
    sticker = ""
    reactions = ""
    ar = []
    sr = []
    if "https://discord.com/channels" in emotes:
        try:
            message_ids = emotes.split('/')
            message = await ctx.bot.rest.fetch_message(message_ids[-2],message_ids[-1])
            if message.stickers:
                sticker = message.stickers
            if message.reactions:
                reactions = message.reactions
            if message.content:
                animated = animated_re.findall(message.content)
                static = static_re.findall(message.content)
        except:
            await ctx.respond(":x: No custom emotes/stickers could be found on that message...")
            return
    else:
        animated = animated_re.findall(emotes)
        static = static_re.findall(emotes)
    embd = []
    images = []

    if not static and not animated and not sticker and not reactions:
        await ctx.respond(":x: No custom emotes/stickers could be found on that message...")
        return
    
    if sticker:
        id = sticker[0].id
        embd = f"https://cdn.discordapp.com/stickers/{id}.png"

        if str(sticker[0].format_type) == "APNG":
            embed = hikari.Embed(description=f"{embd}\n\nPaste URL into https://ezgif.com/apng-to-gif to convert to a GIF")
        else:
            embed = hikari.Embed(description=embd)
        embed.set_image(embd)
        await ctx.respond(embed=embed)
        return

    for r in reactions:
        if animated_re.findall(str(r)):
            ar.append(animated_re.findall(str(r))[0])
        if static_re.findall(str(r)):
            sr.append(static_re.findall(str(r))[0])

    for name, id in sr:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.png")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.png")
    for name, id in ar:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.gif")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.gif")
    for name, id in static:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.png")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.png")
    for name, id in animated:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.gif")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.gif")
    
    for i in range(len(embd)):
        embed = hikari.Embed(description=embd[i])
        embed.set_image(images[i])
        if i == 0:
            await ctx.respond(embed=embed)
        else:
            await ctx.get_channel().send(embed=embed)
    
@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("Steal Emote", "Steal custom emotes from a message.", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def steal(ctx: lightbulb.Context, target: hikari.Message):
    animated = animated_re.findall(target.content)
    static = static_re.findall(target.content)
    embd = []
    images = []

    if not static and not animated:
        await ctx.respond(":x: No custom emojis could be found on that message...")
        return
    
    for name, id in static:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.png")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.png")
    for name, id in animated:
        embd.append(f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.gif")
        images.append(f"https://cdn.discordapp.com/emojis/{id}.gif")
    
    for i in range(len(embd)):
        embed = hikari.Embed(description=embd[i])
        embed.set_image(images[i])
        if i == 0:
            await ctx.respond(embed=embed)
        else:
            await ctx.get_channel().send(embed=embed)
        
def load(bot):
    bot.add_plugin(plugin)