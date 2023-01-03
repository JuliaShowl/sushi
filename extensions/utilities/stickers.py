import hikari
import lightbulb
import re

plugin = lightbulb.Plugin("stickers")
plugin.add_checks(
    lightbulb.guild_only
)

    
@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("Steal Sticker", "Steal sticker from a message.", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def steal(ctx: lightbulb.Context, target: hikari.Message):
    sticker = target.stickers
    embd = ""
    image = ""

    if not sticker:
        await ctx.respond(":x: No custom sticker could be found on that message...")
        return

    id = sticker[0].id
    embd = f"https://cdn.discordapp.com/stickers/{id}.png"
    image = f"https://cdn.discordapp.com/stickers/{id}.png"

    embed = hikari.Embed(description=embd)
    embed.set_image(image)
    await ctx.respond(embed=embed)
        
def load(bot):
    bot.add_plugin(plugin)