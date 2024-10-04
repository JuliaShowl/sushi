import lightbulb
import random
import hikari

from supabase import create_client

url = ""
key = ""
supabase = create_client(url, key)


sush = supabase.table("pets").select("*").eq("type", "sushi").execute()
eg = supabase.table("pets").select("*").eq("type", "egg").execute()
mch = supabase.table("pets").select("*").eq("type", "munchie").execute()

souris = supabase.table("misc").select("*").eq("type", "plant").execute()
brd = supabase.table("misc").select("*").eq("type", "bread").execute()


plugin = lightbulb.Plugin('sheet')

@plugin.command
@lightbulb.command('sushi','Returns a picture of sushi')
@lightbulb.implements(lightbulb.SlashCommand)
async def sushi(ctx):
    global sush
    try: 
        if len(sush.data) > 0:
            i = random.randrange(0,len(sush.data))
            img = sush.data[i]['url']
            sush.data.remove(sush.data[i])
        else:
            sush = supabase.table("pets").select("*").eq("type", "sushi").execute()
            i = random.randrange(0,len(sush))
            img = sush.data[i]['url']
            sush.data.remove(sush.data[i])
        await ctx.respond(img)
    except:
        await ctx.respond("Error with getting image")

@plugin.command
@lightbulb.command('egg','Returns a picture of egg')
@lightbulb.implements(lightbulb.SlashCommand)
async def egg(ctx):
    global eg
    try: 
        if len(eg.data) > 0:
            i = random.randrange(0,len(eg.data))
            img = eg.data[i]['url']
            eg.data.remove(eg.data[i])
        else:
            eg = supabase.table("pets").select("*").eq("type", "egg").execute()
            i = random.randrange(0,len(eg))
            img = eg.data[i]['url']
            eg.data.remove(eg.data[i])
        await ctx.respond(img)
    except:
        await ctx.respond("Error with getting image")
    
@plugin.command
@lightbulb.command('souris_plant','Returns a picture of souris\' plant')
@lightbulb.implements(lightbulb.SlashCommand)
async def souris_plant(ctx):
    global souris
    try: 
        if len(souris.data) > 0:
            i = random.randrange(0,len(souris.data))
            img = souris.data[i]['url']
            souris.data.remove(souris.data[i])
        else:
            souris = supabase.table("misc").select("*").eq("type", "plant").execute()
            i = random.randrange(0,len(souris))
            img = souris.data[i]['url']
            souris.data.remove(souris.data[i])
        await ctx.respond(img)
    except:
        await ctx.respond("Error with getting image")

@plugin.command
@lightbulb.command('munchie','Returns a picture of Munchie and friends')
@lightbulb.implements(lightbulb.SlashCommand)
async def munchie(ctx):
    global mch
    try: 
        if len(mch.data) > 0:
            i = random.randrange(0,len(mch.data))
            img = mch.data[i]['url']
            mch.data.remove(mch.data[i])
        else:
            mch = supabase.table("pets").select("*").eq("type", "munchie").execute()
            i = random.randrange(0,len(mch))
            img = mch.data[i]['url']
            mch.data.remove(mch.data[i])
        await ctx.respond(img)
    except:
        await ctx.respond("Error with getting image")

@plugin.command
@lightbulb.command('bread','Returns a bread')
@lightbulb.implements(lightbulb.SlashCommand)
async def bread(ctx):
    global brd
    try: 
        if len(brd.data) > 0:
            i = random.randrange(0,len(brd.data))
            img = brd.data[i]['url']
            brd.data.remove(brd.data[i])
        else:
            brd = supabase.table("misc").select("*").eq("type", "bread").execute()
            i = random.randrange(0,len(brd))
            img = brd.data[i]['url']
            brd.data.remove(brd.data[i])
        await ctx.respond(img)
    except:
        await ctx.respond("Error with getting image")


@plugin.listener(hikari.GuildMessageCreateEvent)
async def soosh(event):
    global sush
    if event.is_bot:
        return
    try:
        if 'hi sushi' in event.content.lower():
            try:
                if len(sush.data) > 0:
                    i = random.randrange(0,len(sush.data))
                    img = sush.data[i]['url']
                    sush.data.remove(sush.data[i])
                else:
                    sush = supabase.table("pets").select("*").eq("type", "sushi").execute()
                    i = random.randrange(0,len(sush))
                    img = sush.data[i]['url']
                    sush.data.remove(sush.data[i])
                await plugin.bot.rest.create_message(event.channel_id, img)
            except:
                pass
    except:
        pass

@plugin.command
@lightbulb.command('responders', 'Gets all responders and their total entries.', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def responders(ctx: lightbulb.Context):
    try:
        sushi = supabase.table('pets').select('*', count='exact').eq('type', 'sushi').execute().count

        egg = supabase.table('pets').select('*', count='exact').eq('type', 'egg').execute().count

        plant = supabase.table('misc').select('*', count='exact').eq('type', 'plant').execute().count

        munchie = supabase.table('pets').select('*', count='exact').eq('type', 'munchie').execute().count

        bread = supabase.table('misc').select('*', count='exact').eq('type', 'bread').execute().count


        resp_pets = f"Sushi - `{sushi}` entries\nEgg - `{egg}` entries\nMunchie - `{munchie}` entries\n"
        resp_misc = f"Souris_Plant - `{plant}` entries\nBread - `{bread}` entries\n"

        embed = hikari.Embed(title="Sushi Responders")
        embed.add_field("Pets", value=resp_pets)
        embed.add_field("Misc", value=resp_misc)
        await ctx.respond(embed=embed)
    except:
        pass


def load(bot):
    bot.add_plugin(plugin)
