import lightbulb
import hikari
from lightbulb.utils import pag, nav
from lightbulb.utils.pag import EmbedPaginator
from miru.ext import nav

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
 
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
SERVICE_ACCOUNT_FILE = ''
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

plugin = lightbulb.Plugin('youtube')

@plugin.command
@lightbulb.option("query", "Query to search", type=str, required=True)
@lightbulb.option("count", "Number of queries to retreive. (1-50) Default 10", type=int, required=False, min_value=1, max_value=50, default=10)
@lightbulb.command("yt", "Search for YouTube videos")
@lightbulb.implements(lightbulb.SlashCommand)
async def yt(ctx: lightbulb.Context):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
        q=ctx.options.query,
        part='id',
        type='video',
        maxResults=ctx.options.count
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    videos = []

    for search_result in response.get('items', []):
        videos.append(f"https://youtube.com/watch?v={search_result['id']['videoId']}")

    buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
    navigator = nav.NavigatorView(pages=videos, buttons=buttons)
    await navigator.send(ctx.interaction)

@plugin.command
@lightbulb.option("query", "Query to search", type=str, required=True)
@lightbulb.option("count", "Number of queries to retreive. (1-25) Default 5", type=int, required=False, min_value=1, max_value=25, default=5)
@lightbulb.command("yt_stats", "Get statistics for a certain YouTube video")
@lightbulb.implements(lightbulb.SlashCommand)
async def yt_stats(ctx: lightbulb.Context):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
         q=ctx.options.query,
        part='id,snippet',
        type='video',
        maxResults=ctx.options.count
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in response.get('items', []):
        videos.append(search_result['id']['videoId'])

    response = []
    for i in range(len(videos)):  
        responses = youtube.videos().list(id=videos[i],part='snippet,statistics').execute()  
        response.append(responses.get('items', []))

    if not response:
        await ctx.respond("No results found")
        return

    pages = []
    for i in range(len(response)):
        title = response[i][0]['snippet']['title']
        title = title.replace("&quot;", "\"")
        thumbnail = response[i][0]['snippet']['thumbnails']['default']['url']
        views = int(response[i][0]['statistics']['viewCount'])
        views = str("{:,}".format(views))
        likes = int(response[i][0]['statistics']['likeCount'])
        likes = str("{:,}".format(likes))
        comments = int(response[i][0]['statistics']['commentCount'])
        comments = str("{:,}".format(comments))
        stats = f'https://youtube.com/watch?v={videos[i]}\n\n**Views:** {views}\n**Likes:** {likes}\n**Comments:** {comments}'
        embed = hikari.Embed(title = title, description=stats)
        embed.set_thumbnail(thumbnail)
        pages.append(embed)
    
    buttons = [nav.FirstButton(), nav.PrevButton(), nav.StopButton(), nav.NextButton(), nav.LastButton()]
    navigator = nav.NavigatorView(pages=pages, buttons=buttons)
    await navigator.send(ctx.interaction)

def load(bot):
    bot.add_plugin(plugin)
