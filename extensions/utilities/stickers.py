import hikari
import lightbulb

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

    if not sticker:
        await ctx.respond(":x: No custom sticker could be found on that message...")
        return

    id = sticker[0].id
    embd = f"https://cdn.discordapp.com/stickers/{id}.png"

    if str(sticker[0].format_type) == "APNG":
        embed = hikari.Embed(description=f"{embd}\n\nPaste URL into https://ezgif.com/apng-to-gif to convert to a GIF")
    else:
        embed = hikari.Embed(description=embd)
    embed.set_image(embd)
    
    await ctx.respond(embed=embed)
        
def load(bot):
    bot.add_plugin(plugin)