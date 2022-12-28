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
@lightbulb.option("count", "Number of queries to retreive", type=int, required=False, min_value=1, max_value=50, default=10)
@lightbulb.command("yt", "Search for YouTube videos", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def yt(ctx: lightbulb.Context, query: str, count:int):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=count
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in response.get('items', []):
        videos.append(search_result['id']['videoId'])

    paginated = pag.StringPaginator()
    for l in range(len(videos)):
        paginated.add_line(f"https://youtube.com/watch?v={videos[l]}")
        paginated.new_page()
    navigator = nav.ReactionNavigator(paginated.build_pages())
    await navigator.run(ctx)

@plugin.command
@lightbulb.option("query", "Query to search", type=str, required=True)
@lightbulb.option("count", "Number of queries to retreive", type=int, required=False, min_value=1, max_value=25, default=5)
@lightbulb.command("yt_stats", "Get statistics for a certain YouTube video", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def yt_stats(ctx: lightbulb.Context, query: str, count: int):
    youtube = build('youtube', 'v3', credentials=credentials)

    response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=count
    ).execute()

    if not response.get('items'):
        await ctx.respond("No results found")
        return

    videos = []
    titles = []
    views = []
    likes = []
    comments = []
    thumbnails = []

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

    paginated = pag.EmbedPaginator()
    @paginated.embed_factory()
    def build_embed(page_index, page_content):
            page_content = eval(page_content)
            embed = hikari.Embed(title = page_content.get('title'), description= page_content.get('content'))
            embed.set_thumbnail(page_content.get('thumbnail'))
            return embed

    for i in range(len(response)):
        titles.append(response[i][0]['snippet']['title'])
        titles[i] = titles[i].replace("&quot;", "\"")
        resp = {'title': titles[i]}
        thumbnails.append(response[i][0]['snippet']['thumbnails']['default']['url'])
        views.append(int(response[i][0]['statistics']['viewCount']))
        views[i] = str("{:,}".format(views[i]))
        likes.append(int(response[i][0]['statistics']['likeCount']))
        likes[i] = str("{:,}".format(likes[i]))
        comments.append(int(response[i][0]['statistics']['commentCount']))
        comments[i] = str("{:,}".format(comments[i]))
        stats = f'https://youtube.com/watch?v={videos[i]}\n\n**Views:** {views[i]}\n**Likes:** {likes[i]}\n**Comments:** {comments[i]}'
        resp.update({'content': stats})
        resp.update({'thumbnail': thumbnails[i]})
        paginated.add_line(resp)
        paginated.new_page()
    
    navigator = nav.ButtonNavigator(paginated.build_pages())
    await navigator.run(ctx)

def load(bot):
    bot.add_plugin(plugin)
