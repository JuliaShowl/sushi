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
@lightbulb.option("count", "Number of quizzes to generate (1-20) Default 1", type=int, min_value=1, max_value=20,default=1, required=False)
@lightbulb.option("options", "Number of answers to generate (2-6) Default 4", type=int, min_value=2, max_value=6, default=4, required=False)
@lightbulb.command("fq", "Flag quiz", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def flag(ctx: lightbulb.Context, count: int, options: int):
    response = requests.get(f"https://shadify.dev/api/countries/country-quiz?amount={count}&variants={options}")
    quiz = response.json()
    for i in range(count):
        answer = quiz[i]["answer"]
        flag = quiz[i]["flag"]
        view = miru.View(timeout=60)  # Create a new view
        for j in range(options):
            view.add_item(optButtons(quiz[i]["variants"][j], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["variants"][j]))
        embed = hikari.Embed(title="Guess the country")
        embed.set_image(flag)
        message = await ctx.respond(embed=embed, components=view)

        await view.start(message)  # Start listening for interactions

        await view.wait()  # Wait until the view is stopped or times out

        if hasattr(view, "answer"):  # Check if there is an answer
            if view.answer == answer:
                await ctx.respond(f"{answer} is the correct answer!")
            else:
                await ctx.respond(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
        else:
            await ctx.respond(f"Did not receive an answer in time! The correct answer is {answer}.")

def load(bot):
    bot.add_plugin(plugin)