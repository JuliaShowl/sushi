import hikari
import lightbulb
import re

plugin = lightbulb.Plugin("steal")

static_re = re.compile(r"<:([^:]+):(\d+)>")
animated_re = re.compile(r"<a:([^:]+):(\d+)>")    

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("Steal Emoji", "Steal emojis from a message.", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def steal(ctx: lightbulb.Context, target: hikari.Message):
    animated = animated_re.findall(target.content)
    static = static_re.findall(target.content)
    img = ""
    response = ""

    if not static and not animated:
        await ctx.respond(":x: No custom emojis could be found on that message...")
        return
    
    for name, id in static:
        response += f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.png"
        img = f"https://cdn.discordapp.com/emojis/{id}.png"
    for name, id in animated:
        response += f"`:{name}:`\nhttps://cdn.discordapp.com/emojis/{id}.gif"
        img = f"https://cdn.discordapp.com/emojis/{id}.gif"
    
    embed = hikari.Embed(description=response)
    embed.set_image(img)
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(plugin)