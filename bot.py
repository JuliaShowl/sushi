import lightbulb
import hikari

TOKEN = ""
bot = lightbulb.BotApp(token=TOKEN)

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
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.",flags=hikari.MessageFlag.EPHEMERAL,)
    elif isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond(f"You do not have the required role.",flags=hikari.MessageFlag.EPHEMERAL)
    else:
        raise exception

bot.load_extensions_from('./extensions')
bot.run()
