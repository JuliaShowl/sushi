from datetime import datetime
import lightbulb
import hikari
import pytz

plugin = lightbulb.Plugin("user")

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("user", "User to get avatar for", required=True, type=hikari.User)
@lightbulb.command("avatar", "Get the avatar of a user", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def steal(ctx: lightbulb.Context, user: hikari.User):
    embed = hikari.Embed(title=f'{user}\'s Avatar')
    if user.avatar_url:
        embed.set_image(user.avatar_url)
    else:
        embed.set_image(user.default_avatar_url)
    await ctx.respond(embed=embed)
    
@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("user", "User to get stats for", required=True, type=hikari.Member)
@lightbulb.command("whois", "Get stats of a user for this server **WIP**", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def whois(ctx: lightbulb.Context, user: hikari.Member):
    join_at = datetime.strptime(user.joined_at)
    join_date = join_at.astimezone(tz=pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

    embed = hikari.Embed(title=f'{user}\'s Stats', description=join_date)
    if user.avatar_url:
        embed.set_thumbnail(user.avatar_url)
    else:
        embed.set_thumbnail(user.default_avatar_url)
    await ctx.respond(embed=embed)
        
def load(bot):
    bot.add_plugin(plugin)