import lightbulb
import hikari
import requests
import json
import random
import tweepy

# Documentation https://github.com/nidhaloff/deep-translator
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator)


plugin = lightbulb.Plugin('translate')
plugin.add_checks(
    lightbulb.guild_only
)

client = tweepy.Client("CLIENT")

@plugin.command
@lightbulb.option("target", "Target language. If not provided will be English", type=str, required=False)
@lightbulb.option("source","Source language. If not provided will attempt to detect.", type=str, required=False)
@lightbulb.option("text", "Text to translate", type=str, required=True)
@lightbulb.command("translate", "Translate text", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def translate(ctx: lightbulb.Context, text: str, source: str, target: str):
    if "twitter.com" in text:
        global client
        tweet_id = text.split('/')
        tweet_id = tweet_id[-1]
        tweet_id = tweet_id.split('?')
        tweet_id = tweet_id[0]
        response = client.get_tweet(tweet_id)
        text = response[0]["text"]
    if target:
        target = target.lower()
    else:
        target = 'en'
    if source:
        source = source.lower()
    else:
        source = 'auto'
    if source == 'kr' or source == 'korean': source = 'ko'
    if source == 'jp' or source == 'japanese': source = 'ja'
    if target == 'kr' or target == 'korean': target = 'ko'
    if target == 'jp' or target == 'japanses': target = 'ja'

    if source == 'ko' or target == 'ko' or source == 'ja' or target == 'ja':
        client, secret = random.choice(list(dict.items()))
        payload = {"source": source, "target": target, "text": text}
        headers = {
            "X-Naver-Client-Id": client,
            "X-Naver-Client-Secret": secret,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        try: 
            response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=payload)
            res_body = json.loads(response.text)
            msg = res_body.get("message")
            result = msg.get("result", None)
            if not result:
                translator = GoogleTranslator(source=source, target=target)
                result = translator.translate(text)
                await ctx.respond(f'{text} -> {result}')
                return
                
            result = result.get("translatedText")
            await ctx.respond(f'{text} -> {result}')
            return
        except:
            pass
    else:
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