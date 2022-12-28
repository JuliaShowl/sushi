import lightbulb
import hikari

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help','List commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    sushi = "`/sushi` - Returns a picture of Sushi, Mia's hamster\n"
    egg = "`/egg` - Returns a picture of Egg, Souris' cat\n"
    plant = "`/souris_plant` - Returns a picture of Souris' bonsai or some random Reddit plant\n"
    munchie = "`/munchie` - Returns a picture of Munchie.\n"
    add = "`/add <responder> <media>` - Adds media to database.\n"
    remove = "`/remove <media>` - Removes media from database.\n"
    zim = "`/zimzalabim` - Are you ready for this?\n"
    pan = "`/pantomime` - Like a pantomime\n"
    math = "`/solve <equation>` - Solves equations. Supports python's math library\n"
    meme = "`/meme` - Gets random reddit meme"
    yoink = "`/yoihnk <emotes>` - Grabs custom emotes\n"
    yt = "`/yt <query> <count|optional>` - Search for YouTube videos. Count: Min 1, Max 50, Default 10\n"
    yt_stats = "`/yt_stats <query> <count|optional>` - Get statistics for a YouTube video. Count: Min 1, Max 25, Default 5\n"
    resp = f"**Media Responders**\n{sushi}{egg}{munchie}{plant}{zim}{pan}{add}{remove}\n**Misc Responders**\n{math}{meme}\n**Utilities**\n{yoink}{yt}{yt_stats}"
    embed = hikari.Embed(title="SushiBot Help",description=resp, color='b0ffe3')
    await ctx.respond(embed=embed)
def load(bot):
    bot.add_plugin(plugin)
