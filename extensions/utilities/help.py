import lightbulb
import hikari
from miru.ext import nav

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help','List commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    help = []
    embed = hikari.Embed(title="SushiBot Help", color='b0ffe3')
    sushi = "`/sushi` - Returns a picture of Sushi, Mia's hamster\n"
    egg = "`/egg` - Returns a picture of Egg, Souris' cat\n"
    plant = "`/souris_plant` - Returns a picture of Souris' bonsai or some random Reddit plant\n"
    munchie = "`/munchie` - Returns a picture of Munchie and Friends.\n"
    bread = "`/bread` - Returns a picture of bread.\n"
    pic = "`/pic <query> <quantity|optional>` - Get pictures!\n"
    add = "`/add <responder> <media>` - Adds media to database. Supports embeddable links, discord messages, and tweets.\n"
    remove = "`/remove <media> <responder|optional>` - Removes media from database.\n"
    moon = "`/moonlightsunrise` - Baby come be my starlight\n"
    zim = "`/zimzalabim` - Are you ready for this?\n"
    pan = "`/pantomime` - Like a pantomime\n"
    math = "`/solve <equation>` - Solves equations. Supports python's math library\n"
    meme = "`/meme <sub|optional>` - Gets a random reddit meme\n"
    dadjoke = "`/dadjoke` - Get a random dad joke.\n"
    yoink = "`/yoink <emotes/message link>` - Grabs custom emotes and stickers.\n"
    yt = "`/yt <query> <count|optional>` - Search for YouTube videos.\n"
    yt_stats = "`/yt_stats <query> <count|optional>` - Get statistics for a YouTube video.\n"
    avatar = "`/avatar <user|optional> <type|optional>` - Gets the avatar of a user.\n"
    translate = "`/translate <query> <source|optional> <target|optional>` - Translate strings.\n"
    languages = "`/lnguages` - Get a list of supported languages.\n"
    twt = "`/twt <tweet>` - Get media from a tweet.\n"
    search = "`/search <query>` - Search the web.\n"
    whois = "`/whois <user|optional>` - Get information about a user.\n"
    serverinfo = "`/serverinfo` - Get information about the server.\n"
    choose = "`/choose <option1> <option2>` - Choose between two options.\n"
    convert = "`/convert <number> <unit1> <unit2>` - Convert between units. *Some calculations are approximations*"
    embed.add_field("Media Responders", value=f"{sushi}{egg}{munchie}{plant}{bread}{moon}{zim}{pan}{pic}{add}{remove}")
    embed.add_field("Misc Responders", value=f"{math}{meme}{dadjoke}")
    embed.add_field("Utilities", value=f"{translate}{languages}{search}{twt}{yoink}{yt}{yt_stats}{avatar}{whois}{serverinfo}{choose}{convert}")
    help.append(embed)

    embed = hikari.Embed(title="SushiBot Help", color='b0ffe3')
    fq = "`/fq <count|optional> <options|optional>` - Guess the flag\n"
    cq = "`/cq <count|optional> <options|optional>` - Guess the capital\n"
    trivia = "`/trivia <count|optional> <category|optional> <difficulty|optional>` - Get trivia questions\n"
    vs = "`/vs <type> <count|optional> <category|optional> <difficulty|optional> <options|optional>` - Play the quizzes against friends.\n"
    rps = "`/rps <players|optional> <user|optional>` - Play rock, paper, scissors against Sushi or a friend!\n"
    embed.add_field("Games", value=f"{fq}{cq}{trivia}{vs}{rps}")
    help.append(embed)

    buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
    navigator = nav.NavigatorView(pages=help, buttons=buttons)
    await navigator.send(ctx.interaction)
def load(bot):
    bot.add_plugin(plugin)
