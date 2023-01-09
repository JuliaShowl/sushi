from time import sleep
from tokenize import String
import lightbulb
import hikari

plugin = lightbulb.Plugin('fakeban')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command()
@lightbulb.add_cooldown(5.0,1,lightbulb.UserBucket)
@lightbulb.option("reason", "Reason for **fake** banning member", type=str, required=False, default="Not specified")
@lightbulb.option("user", "User you want to **fake** ban", type=hikari.User,required=True)
@lightbulb.command("bans", "**Fake** bans a user", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def bans(ctx: lightbulb.Context, user: hikari.User, reason: str):
    await ctx.respond(f"Banning **{user}**")
    sleep(1)
    await ctx.edit_last_response(f"{user.mention} has been banned for `{reason}`")

def load(bot):
    bot.add_plugin(plugin)
