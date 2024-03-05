import lightbulb
import hikari
import requests
import json
import random

# Documentation https://github.com/nidhaloff/deep-translator
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeeplTranslator,
                             QcriTranslator)


plugin = lightbulb.Plugin('translate')
plugin.add_checks(
    lightbulb.guild_only
)

@plugin.command
@lightbulb.option("target", "Target language. If not provided will be English", type=str, required=False)
@lightbulb.option("source","Source language. If not provided will attempt to detect.", type=str, required=False)
@lightbulb.option("text", "Text to translate", type=str, required=True)
@lightbulb.command("translate", "Translate text", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def translate(ctx: lightbulb.Context, text: str, source: str, target: str):
    if "twitter.com" in text or "x.com" in text:
        global client
        tweet_id = text.split('/')
        tweet_id = tweet_id[-1]
        tweet_id = tweet_id.split('?')
        tweet_id = tweet_id[0]
        try:
            response = requests.get(f'https://api.vxtwitter.com/Twitter/status/{tweet_id}')
        except:
            await ctx.resolved("Unable to get that tweet.")
        text = response.json().get('text')
    if target:
        target = target.lower()
    else:
        target = 'en'
    if source:
        source = source.lower()
    else:
        source = 'auto'

        translator = GoogleTranslator(source=source, target=target)
    try:
        result = translator.translate(text)
        
        await ctx.respond(f'{text} -> {result}')
    except:
        await ctx.respond("Unable to translate.")

@plugin.command
@lightbulb.command("languages", "Get a list of supported languages", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def langauges(ctx: lightbulb.context):
    langs_list = GoogleTranslator.get_supported_languages(as_dict=True)
    langs = ""
    for l, a in langs_list.items():
        langs = langs + "`(" + a + ")` - " + l + "\n"
    embed = hikari.Embed(title="Supported Languages", description=langs)
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(plugin)