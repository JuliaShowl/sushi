import requests
import hikari
import lightbulb
import miru
import random

plugin = lightbulb.Plugin("trivia")
plugin.add_checks(
    lightbulb.guild_only
)

class optButtons(miru.Button):
    # Let's leave our arguments dynamic this time, instead of hard-coding them
    def __init__(self, choice, author, *args, **kwargs) -> None:
        self.choice = choice
        self.author = author
        super().__init__(*args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        if ctx.user.id == self.author:
            self.view.answer = self.choice
            self.view.stop()
        else:
            await ctx.respond("You did not generate this question", flags=hikari.MessageFlag.EPHEMERAL)

@plugin.command()
@lightbulb.option("count", "Number of quizzes to generate (1-20) Default 1", type=int, min_value=1, max_value=20,default=1,required=False)
@lightbulb.option("category", "Category for the question", type=str, choices=['arts_and_literature', 'film_and_tv', 'food_and_drink', 'general_knowledge', 'geography', 'history', 'music', 'science', 'society_and_culture', 'sport_and_lesiure'], required=False, default=None)
@lightbulb.option("difficulty", "Difficulty of the question", type=str, choices=['easy', 'medium', 'hard'], required=False, default=None)
@lightbulb.command("trivia", "Get a trivia question", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def sudoku(ctx: lightbulb.Context, count: int, category: str, difficulty: str):
    if category is None and difficulty is None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?limit={count}")
    elif category is not None and difficulty is None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?categories={category}&limit={count}")
    elif category is None and difficulty is not None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?diffculty={difficulty}&limit={count}")
    else:
        response = requests.get(f"https://the-trivia-api.com/api/questions?diffculty={difficulty}&categories={category}&limit={count}")
    quiz = response.json()
    score = 0
    for i in range(count):
        answer = quiz[i]["correctAnswer"]
        question = quiz[i]["question"]
        view = miru.View(timeout=60)  # Create a new view
        a0 = optButtons(quiz[i]["correctAnswer"], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["correctAnswer"])
        a1 = optButtons(quiz[i]["incorrectAnswers"][0], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][0])
        a2 = optButtons(quiz[i]["incorrectAnswers"][1], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][1])
        a3 = optButtons(quiz[i]["incorrectAnswers"][2], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["incorrectAnswers"][2])
        answers = [a0, a1, a2, a3]
        new_list = random.sample(answers, 4)
        for j in new_list:
            view.add_item(j)
        message = await ctx.respond(f"**{question}**", components=view)

        await view.start(message)  # Start listening for interactions

        await view.wait()  # Wait until the view is stopped or times out

        if hasattr(view, "answer"):  # Check if there is an answer
            if view.answer == answer:
                score += 1
                await ctx.respond(f"{answer} is the correct answer!")
            else:
                await ctx.respond(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
        else:
            await ctx.respond(f"Did not receive an answer in time! The correct answer is {answer}.")
    if count > 1:
        await ctx.respond(f"Total score: **{score}/{count}**")

def load(bot):
    bot.add_plugin(plugin)