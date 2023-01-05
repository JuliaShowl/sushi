import requests
import hikari
import lightbulb
import miru
import random

plugin = lightbulb.Plugin("sudoku")
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

@plugin.command()
@lightbulb.option("count", "Number of quizzes to generate (1-20) Default 1", type=int, min_value=1, max_value=20,default=1)
@lightbulb.command("trivia", "Get a trivia question", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def sudoku(ctx: lightbulb.Context, count: int):
    response = requests.get(f"https://the-trivia-api.com/api/questions?limit={count}")
    quiz = response.json()
    for i in range(count):
        answer = quiz[i]["correctAnswer"]
        question = quiz[i]["question"]
        view = miru.View(timeout=60)  # Create a new view
        a0 = optButtons(quiz[i]["correctAnswer"], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["correctAnswer"])
        a1 = optButtons(quiz[i]["incorrectAnswers"][0], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][0])
        a2 = optButtons(quiz[i]["incorrectAnswers"][1], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][1])
        a3 = optButtons(quiz[i]["incorrectAnswers"][2], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][2])
        answers = [a0, a1, a2, a3]
        new_list = random.sample(answers, 4)
        for j in new_list:
            view.add_item(j)
        embed = hikari.Embed(title=question)
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