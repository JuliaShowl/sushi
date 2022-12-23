from tokenize import String
import lightbulb
import hikari

plugin = lightbulb.Plugin('vids')

@plugin.command
@lightbulb.command('zimzalabim','Are you ready for this?')
@lightbulb.implements(lightbulb.SlashCommand)
async def zimzalabim(ctx):
    f = hikari.File('./media/zimzalabim.mp4')
    await ctx.respond(f)

@plugin.command
@lightbulb.command('pantomime','Like a pantomime')
@lightbulb.implements(lightbulb.SlashCommand)
async def pantomime(ctx):
    f = hikari.File('./media/pantomime.mp4')
    await ctx.respond(f)

def load(bot):
    bot.add_plugin(plugin)
