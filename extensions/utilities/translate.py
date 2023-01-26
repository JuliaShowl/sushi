import lightbulb
import hikari
import requests
import json
import random

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

@plugin.command
@lightbulb.option("target", "Target language. If not provided will be English", type=str, required=False)
@lightbulb.option("source","Source language. If not provided will attempt to detect.", type=str, required=False)
@lightbulb.option("query", "Query to translate", type=str, required=True)
@lightbulb.command("translate", "Translate text", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def translate(ctx: lightbulb.Context, query: str, source: str, target: str):
    target = target or 'en'
    if source == 'kr': source = 'ko'
    if source == 'jp': source = 'ja'
    if target == 'kr': target = 'ko'
    if target == 'jp': target = 'ja'

    if source == 'ko' or source == 'korean' or target == 'ko' or target == 'korean' or source == 'ja' or source == "japanese" or target == 'ja' or target == "japanese":
        client, secret = random.choice(list(dict.items()))
        payload = {"source": source, "target": target, "text": query}
        headers = {
            "X-Naver-Client-Id": client,
            "X-Naver-Client-Secret": secret,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        response = requests.post('https://openapi.naver.com/v1/papago/n2mt', headers=headers, data=payload)
        res_body = json.loads(response.text)
        msg = res_body.get("message")
        result = msg.get("result", None)
        if not result:
            translator = GoogleTranslator(source=source, target=target)
            result = translator.translate(query)
            await ctx.respond(f'{query} -> {result}')
            return
            
        result = result.get("translatedText")
        await ctx.respond(f'{query} -> {result}')
        return
    elif source is not None:
        translator = GoogleTranslator(source=source, target=target)
    else:
        translator = GoogleTranslator(source='auto', target=target)

    try:
        result = translator.translate(query)
        
        await ctx.respond(f'{query} -> {result}')
    except:
        await ctx.respond("Unable to translate.")

@plugin.command
@lightbulb.command("languages", "Get a list of supported languages", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def langauges(ctx: lightbulb.context, translator: str):
    langs_list = GoogleTranslator.get_supported_languages(as_dict=True)
    langs = ""
    for l, a in langs_list.items():
        langs = langs + "`(" + a + ")` - " + l + "\n"
    embed = hikari.Embed(title="Supported Languages", description=langs)
    await ctx.respond(embed=embed)



def load(bot):
    bot.add_plugin(plugin)