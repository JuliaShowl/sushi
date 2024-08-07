import lightbulb
import hikari
import miru

TOKEN = ""
bot = lightbulb.BotApp(token=TOKEN)
client = miru.Client(bot)

@bot.command
@lightbulb.command('ping','Says pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('Pong!')

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("Only the owner of the bot can use that command.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after}` seconds.")
    elif isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond(f"You do not have the required role(s), `{exception.missing_roles}`.")
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(f"You do not have the required permission(s), `{exception.missing_perms}`.")
    elif isinstance(exception, lightbulb.BotMissingRequiredPermission):
        await event.context.respond(f"This bot does not have the required permission(s), `{exception.missing_perms}`.")
    elif isinstance(exception, lightbulb.OnlyInGuild):
        await event.context.respond("This command can only be used in servers.")
    else:
        raise exception

@bot.command
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command('sync', "Sync commands", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def manualSync(ctx: lightbulb.Context) -> None:
    extensionList = []
    for i in range(len(bot.extensions)):
        extension = bot.extensions[i]
        try:
            bot.reload_extensions(extension)
        except:
            pass
        extensionList.append(extension)
    await bot.sync_application_commands()
    await ctx.respond(f"Reloaded {extensionList}", flags=hikari.MessageFlag.EPHEMERAL)

bot.load_extensions_from("./extensions/", recursive=True)
bot.run()
