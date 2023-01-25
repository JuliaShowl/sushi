import lightbulb
import hikari
from miru.ext import nav

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help','List commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    help = []
    sushi = "`/sushi` - Returns a picture of Sushi, Mia's hamster\n"
    egg = "`/egg` - Returns a picture of Egg, Souris' cat\n"
    plant = "`/souris_plant` - Returns a picture of Souris' bonsai or some random Reddit plant\n"
    munchie = "`/munchie` - Returns a picture of Munchie.\n"
    pic = "`/pic <query> <quantity|optional>` - Get pictures!\n"
    add = "`/add <responder> <media>` - Adds media to database.\n"
    remove = "`/remove <media>` - Removes media from database.\n"
    zim = "`/zimzalabim` - Are you ready for this?\n"
    pan = "`/pantomime` - Like a pantomime\n"
    math = "`/solve <equation>` - Solves equations. Supports python's math library\n"
    meme = "`/meme <sub|optional>` - Gets a random reddit meme\n"
    yoink = "`/yoink <emotes>` - Grabs custom emotes.\n"
    yt = "`/yt <query> <count|optional>` - Search for YouTube videos.\n"
    yt_stats = "`/yt_stats <query> <count|optional>` - Get statistics for a YouTube video.\n"
    avatar = "`/avatar <user>` - Gets the avatar of a user.\n"
    whois = "`/whois <user>` - Gets the statistics of a given user **WIP**.\n"
    helpresp = f"**Media Responders**\n{sushi}{egg}{munchie}{plant}{zim}{pan}{pic}{add}{remove}\n**Misc Responders**\n{math}{meme}\n**Utilities**\n{yoink}{yt}{yt_stats}{avatar}{whois}"
    help.append(hikari.Embed(title="SushiBot Help",description=helpresp, color='b0ffe3'))

    fq = "`/fq <count|optional> <options|optional>` - Guess the flag\n"
    cq = "`/cq <count|optional> <options|optional>` - Guess the capital\n"
    trivia = "`/trivia <count|optional> <category|optional> <difficulty|optional>` - Get trivia questions\n"
    vs = "`/vs <type> <count|optional> <category|optional> <difficulty|optional> <options|optional>` - Play the quizzes against friends.\n"
    rps = "`/rps <players|optional> <user|optional>` - Play rock, paper, scissors against Sushi or a friend!\n"
    gameresp = f"**Games**\n{fq}{cq}{trivia}{vs}{rps}"
    help.append(hikari.Embed(title="SushiBot Help",description=gameresp, color='b0ffe3'))

    buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
    navigator = nav.NavigatorView(pages=help, buttons=buttons)
    await navigator.send(ctx.interaction)
def load(bot):
    bot.add_plugin(plugin)
