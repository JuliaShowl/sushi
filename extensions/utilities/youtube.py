from tokenize import String
import lightbulb
import hikari
from lightbulb.utils import pag, nav

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
@lightbulb.command("yt", "Search for YouTube videos", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def yt(ctx: lightbulb.Context, query: str):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=50
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in response.get('items', []):
        videos.append(search_result['id']['videoId'])

    paginated_help = pag.StringPaginator()
    for l in range(len(videos)):
        paginated_help.add_line(f"https://youtube.com/watch?v={videos[l]}")
        paginated_help.new_page()
    navigator = nav.ReactionNavigator(paginated_help.build_pages())
    await navigator.run(ctx)

@plugin.command
@lightbulb.option("query", "Query to search", type=str, required=True)
@lightbulb.command("yt_stats", "Get statistics for a certain YouTube video", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def yt_stats(ctx: lightbulb.Context, query: str):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=1
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    video = ''
    title = ''

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    video = response.get('items', [])
    video = video[0]['id']['videoId']
    
    response = youtube.videos().list(
        id=video,
        part='snippet,statistics'
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return
    response = response.get('items', [])
    title = response[0]['snippet']['title']
    title = title.replace("&quot;", "\"")
    thumbnail = response[0]['snippet']['thumbnails']['default']['url']
    views = int(response[0]['statistics']['viewCount'])
    views = str("{:,}".format(views))
    likes = int(response[0]['statistics']['likeCount'])
    likes = str("{:,}".format(likes))
    comments = int(response[0]['statistics']['commentCount'])
    comments = str("{:,}".format(comments))
    resp = f'https://youtube.com/watch?v={video}\n\n**Views:** {views}\n**Likes:** {likes}\n**Comments:** {comments}'
    embed = hikari.Embed(title=f'View count for {title}', description=resp)
    embed.set_thumbnail(thumbnail)
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(plugin)
