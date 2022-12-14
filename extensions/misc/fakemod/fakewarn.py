import lightbulb
import hikari

plugin = lightbulb.Plugin('fakewarn')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.add_cooldown(5.0,1,lightbulb.UserBucket)
@lightbulb.option('user','The user to **fake** warn', type=hikari.User, required=True)
@lightbulb.option('reason','Reason for **fake** warning',type=str,required=False,default='Not specified')
@lightbulb.command('warns','**Fake** warn a user', auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def warns(ctx: lightbulb.Context, user: hikari.User, reason: str):
    resp = f"{user.mention} has been warned for `{reason}`"
    await ctx.respond(resp)

def load(bot):
    bot.add_plugin(plugin)
