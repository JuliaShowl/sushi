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
@lightbulb.command("yoink", "Steal emojis from a message.", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def steal(ctx: lightbulb.Context, emotes: hikari.Message):
    animated = animated_re.findall(emotes)
    static = static_re.findall(emotes)
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
    
@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("Steal Emote", "Steal custom emotes from a message.", auto_defer=True, pass_options=True)
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