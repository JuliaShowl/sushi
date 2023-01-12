import asyncio
import lightbulb
import hikari

plugin = lightbulb.Plugin('fakekick')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command()
@lightbulb.add_cooldown(5.0,1,lightbulb.UserBucket)
@lightbulb.option("reason", "Reason for **fake** kicking member", type=str, required=False, default="Not specified")
@lightbulb.option("user", "User you want to **fake** kick", type=hikari.User,required=True)
@lightbulb.command("kicks", "**Fake** kicks a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def kicks(ctx: lightbulb.Context, user: hikari.User, reason: str):
    await ctx.respond(f'Attempting to kick **{user}**.')
    await asyncio.sleep(1)
    await ctx.edit_last_response(f"{user.mention} has been kicked for `{reason}`")

def load(bot):
    bot.add_plugin(plugin)
