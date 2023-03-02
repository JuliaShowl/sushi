import lightbulb
from revChatGPT.V1 import Chatbot

plugin = lightbulb.Plugin('chatbot')
plugin.add_checks(
    lightbulb.guild_only
)

# Credentials for OpenAI
gptbot = Chatbot(config={   
    "email": "email@email.com",
    "password": "password"
})

@plugin.command
@lightbulb.option("prompt", "Talk to the bot.", type=str, required=True)
@lightbulb.command('chat','Start a chatbot session', pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def chatbot(ctx: lightbulb.context, prompt: str):
    try:
        for data in gptbot.ask(
            prompt
            ):
                response = data["message"]
        await ctx.respond(response)
    except Exception as e:
        await ctx.respond(e)

def load(bot):
    bot.add_plugin(plugin)