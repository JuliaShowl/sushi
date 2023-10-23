import calendar
import lightbulb
import hikari

plugin = lightbulb.Plugin("user")
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option("type", "Get server avatar or global avatar. Default server avatar", type=str, required=False, choices=["Server", "Global"])
@lightbulb.option("user", "User to get avatar for", required=False, type=hikari.User)
@lightbulb.command("avatar", "Get the avatar of a user", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context, type: str, user: hikari.User):
    if user is None:
        gld = ctx.get_guild()
        user = await ctx.bot.rest.fetch_member(gld, ctx.author)
    usr = await ctx.bot.rest.fetch_user(user)
    ur = str(usr)
    type = type or "Server"
    if type == "Server":
        try:
            embed = hikari.Embed(title=f'{ur}\'s {type} Avatar', color = usr.accent_color)
            embed.set_image(user.guild_avatar_url)
        except:
            embed = hikari.Embed(title=f'{ur}\'s Global Avatar', color = usr.accent_color)
            if user.avatar_url:
                embed.set_image(user.avatar_url)
            else:
                embed.set_image(user.default_avatar_url)
    else:
        embed = hikari.Embed(title=f'{ur}\'s {type} Avatar', color = usr.accent_color)
        if user.avatar_url:
            embed.set_image(user.avatar_url)
        else:
            embed.set_image(user.default_avatar_url)
    await ctx.respond(embed=embed)
    
@plugin.command
@lightbulb.option("user", "User to get stats for", required=False, type=hikari.Member)
@lightbulb.command("whois", "Get stats of a user for this server", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def whois(ctx: lightbulb.Context, user: hikari.Member):
    if user is None:
        user = await ctx.bot.rest.fetch_member(ctx.get_guild(), ctx.author)
    else:
        user = await ctx.bot.rest.fetch_member(ctx.get_guild(), user)
    roles = await user.fetch_roles()
    roles = sorted(roles, key=lambda x: x.position, reverse=True)
    rol = []
    for r in roles:
        if r.color:
            color = r.color
            break
    for r in roles[:-1]:
        rol.append(r.mention)

    join_at = user.joined_at
    join_date = calendar.timegm(join_at.utctimetuple())

    usr = await ctx.bot.rest.fetch_user(user)
    ur = str(usr)
    embed = hikari.Embed(title=f'{ur}', description=user.mention, color=color)
    embed.add_field("Guild Join Date", value=f"<t:{join_date}>",inline=True)

    mbrs = await ctx.bot.rest.fetch_members(ctx.get_guild())
    members = sorted(mbrs, key=lambda m: m.joined_at, reverse=False)
    embed.add_field("Join Position",value=f"{str(members.index(user)+1)}/{len(members)}",inline=True)

    create_at = user.created_at
    create_date = calendar.timegm(create_at.utctimetuple())
    embed.add_field("Account Creation Date", value=f"<t:{create_date}>", inline=False)
    

    boost = user.premium_since
    if boost is not None:
        boost_date = calendar.timegm(boost.utctimetuple())
        embed.add_field("Boosting Since", value=f"<t:{boost_date}>",inline=True)
    else:
        boost_date = "Not boosting"
        embed.add_field("Boosting Since", value=boost_date, inline=True)

    role = " ".join(str(x) for x in rol) 
    if len(role) > 1024:
        role = role[:1018]
        idx = role.rfind(" ")
        role = role[:idx] + " etc."
    embed.add_field(f"Roles [{len(rol)}]", value=role,inline=False)

    if user.guild_avatar_url:
        embed.set_thumbnail(user.guild_avatar_url)
    elif user.avatar_url:
        embed.set_thumbnail(user.avatar_url)
    else:
        embed.set_thumbnail(user.default_avatar_url)
    embed.set_footer(f"ID: {user.id}")
    
    await ctx.respond(embed=embed)
        
def load(bot):
    bot.add_plugin(plugin)
