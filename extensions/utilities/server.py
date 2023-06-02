import calendar
import lightbulb
import hikari

plugin = lightbulb.Plugin("server")
plugin.add_checks(
    lightbulb.guild_only
)

    
@plugin.command
@lightbulb.command("serverinfo", "Get information on the server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def whois(ctx: lightbulb.Context):
    guild = ctx.get_guild()
    roles = await ctx.bot.rest.fetch_roles(guild)
    roles = sorted(roles, key=lambda x: x.position, reverse=True)
    rol = []
    for r in roles:
        if r.color:
            color = r.color
            break
    for r in roles:
        rol.append(r.mention)
    embed = hikari.Embed(title=f"{guild}", color=color)
    owner = await guild.fetch_owner()
    embed.add_field("Owner", value=owner.mention, inline=True)

    members = await ctx.bot.rest.fetch_members(ctx.guild_id).count()
    embed.add_field("Members", value=members, inline=True)

    embed.add_field("Roles", value=len(roles), inline=True)

    channels = await ctx.bot.rest.fetch_guild_channels(guild)
    categories = 0
    text = 0
    voice = 0
    for c in channels:
        if c.type == hikari.ChannelType.GUILD_CATEGORY:
            categories += 1
        if c.type == hikari.ChannelType.GUILD_TEXT or c.type == hikari.ChannelType.GUILD_NEWS:
            text += 1
        if c.type == hikari.ChannelType.GUILD_VOICE:
            voice += 1
    embed.add_field("Category Channels", value=categories, inline=True)
    embed.add_field("Text Channels", value=text, inline=True)
    embed.add_field("Voice Channels", value=voice, inline=True)

    emotes = await guild.fetch_emojis()
    embed.add_field("Emotes", value=len(emotes), inline=True)

    stickers = await guild.fetch_stickers()
    embed.add_field("Stickers", value=len(stickers), inline=True)

    boosters = guild.premium_subscription_count
    embed.add_field("Boosts", value=boosters, inline=True)

    create_date = calendar.timegm(guild.created_at.utctimetuple())
    embed.add_field(f"Guild Create Date", value=f"<t:{create_date}>",inline=False)

    role = " ".join(str(x) for x in rol) 
    if len(role) > 1024:
        role = role[:1018]
        idx = role.rfind(" ")
        role = role[:idx] + " etc."
    embed.add_field(f"Roles List", value=role,inline=False)
    
    embed.set_thumbnail(guild.icon_url)

    embed.set_footer(f"ID: {ctx.guild_id}")

    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
