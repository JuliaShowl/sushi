from time import sleep
import lightbulb
import hikari
import requests

from supabase import create_client

url = ""
key = ""
supabase = create_client(url, key)

plugin = lightbulb.Plugin('source')

@plugin.command
@lightbulb.command("Source", "Get the source of an image", pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def source(ctx: lightbulb.Context, target: hikari.Message):
    try:
        pets = supabase.table("pets").select("source").eq("url", target.content).execute().data
        misc = supabase.table("misc").select("source").eq("url", target.content).execute().data
        if pets:
            await ctx.respond(pets[0]['source'])
        if misc:
            await ctx.respond(misc[0]['source'])
        else:
            await ctx.respond("No source data for image.")
    except Exception as e:
        await ctx.respond(e)

def load(bot):
    bot.add_plugin(plugin)
