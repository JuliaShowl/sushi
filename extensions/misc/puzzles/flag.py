import lightbulb
import hikari
import miru
import requests

plugin = lightbulb.Plugin("flag")
plugin.add_checks(
    lightbulb.guild_only
)

class optButtons(miru.Button):
    # Let's leave our arguments dynamic this time, instead of hard-coding them
    def __init__(self, choice, *args, **kwargs) -> None:
        self.choice = choice
        super().__init__(*args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        self.view.answer = self.choice
        self.view.stop()

@plugin.command
@lightbulb.option("options", "Number of answers to generate (2-6) Default 4", type=int, min_value=2, max_value=6, default=4)
@lightbulb.command("fq", "Flag quiz", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def flag(ctx: lightbulb.Context, options: int):
    response = requests.get(f"https://shadify.dev/api/countries/country-quiz?variants={options}")
    quiz = response.json()
    answer = quiz["answer"]
    view = miru.View()  # Create a new view
    for i in range(options):
        view.add_item(optButtons(quiz["variants"][i], style=hikari.ButtonStyle.PRIMARY, label=quiz["variants"][i]))
    message = await ctx.respond(quiz["flag"], components=view)

    await view.start(message)  # Start listening for interactions

    await view.wait()  # Wait until the view is stopped or times out

    if hasattr(view, "answer"):  # Check if there is an answer
        if view.answer == answer:
            await ctx.respond(f"{answer} is the correct answer!")
        else:
            await ctx.respond(f"The correct answer is {answer}")
    else:
        await ctx.respond(f"Did not receive an answer in time! The correct answer is {answer}")

def load(bot):
    bot.add_plugin(plugin)