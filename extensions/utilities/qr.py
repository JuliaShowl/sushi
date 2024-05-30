import lightbulb
import qrcode
import hikari
import random
import os, sys


plugin = lightbulb.Plugin('qr')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option('text', "Text", type=str, required=True)
@lightbulb.command('qr','Generate a QR Code', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def qr(ctx: lightbulb.Context, text: str):
    try:
        img = qrcode.make(text)
        title = f"sushi{random.randrange(0,sys.maxsize)}.png"
        img.save(title)
        f = hikari.File(f'{title}')
        await ctx.respond(f)
        os.remove(title)
    except:
        await ctx.respond("Unable to generate QR code.")

def load(bot):
    bot.add_plugin(plugin)
