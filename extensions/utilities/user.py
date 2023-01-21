from datetime import datetime
import lightbulb
import hikari
import pytz

plugin = lightbulb.Plugin("user")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("type", "Get server avatar or global avatar. Default server avatar", type=str, required=False, choices=["server", "global"])
@lightbulb.option("user", "User to get avatar for", required=True, type=hikari.User)
@lightbulb.command("avatar", "Get the avatar of a user", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context, type: str, user: hikari.User):
    embed = hikari.Embed(title=f'{user}\'s Avatar')
    type = type or "server"
    if type == "server":
        if user.guild_avatar_url:
            embed.set_image(user.guild_avatar_url)
        elif user.avatar_url:
            embed.set_image(user.avatar_url)
        else:
            embed.set_image(user.default_avatar_url)
    else:
        if user.avatar_url:
            embed.set_image(user.avatar_url)
        else:
            embed.set_image(user.default_avatar_url)
    await ctx.respond(embed=embed)
    
def load(bot):
    bot.add_plugin(plugin)