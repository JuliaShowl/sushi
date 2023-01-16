import requests
import hikari
import lightbulb
import miru
import random

plugin = lightbulb.Plugin("versus")
plugin.add_checks(
    lightbulb.guild_only
)

class optButtons(miru.Button):
    def __init__(self, choice, *args, **kwargs) -> None:
        self.choice = choice
        super().__init__(*args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        self.view.answer = self.choice
        self.view.author = ctx.user.id
        self.view.stop()


@plugin.command()
@lightbulb.option("count", "Number of quizzes to generate (1-20) Default 5", type=int, min_value=1, max_value=20,default=5,required=False)
@lightbulb.option("category", "Category for the question. Only applicable to Trivia.", type=str, choices=['arts_and_literature', 'film_and_tv', 'food_and_drink', 'general_knowledge', 'geography', 'history', 'music', 'science', 'society_and_culture', 'sport_and_lesiure'], required=False, default=None)
@lightbulb.option("difficulty", "Difficulty of the question. Only applicable to Trivia", type=str, choices=['easy', 'medium', 'hard'], required=False, default=None)
@lightbulb.option("options", "Number of answers to generate. Only applicable to Flag Quiz and Capital Quiz (2-6) Default 4", type=int, min_value=2, max_value=6, required=False)
@lightbulb.option("type", "Type of game to play", type=str, required=True, choices=["Trivia", "Flag Quiz", "Capital Quiz"])
@lightbulb.command("vs", "Play games against others", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def vs(ctx: lightbulb.Context, type: str, count: int, category: str, difficulty: str, options: int):
    if type == "Trivia":
        await trivia(ctx, count, category, difficulty)
    if type == "Flag Quiz":
        await fq(ctx, count, options)
    if type == "Capital Quiz":
        await cq(ctx, count, options)

async def trivia(ctx, count, category, difficulty):
    if category is None and difficulty is None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?limit={count}")
    elif category is not None and difficulty is None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?categories={category}&limit={count}")
    elif category is None and difficulty is not None:
        response = requests.get(f"https://the-trivia-api.com/api/questions?diffculty={difficulty}&limit={count}")
    else:
        response = requests.get(f"https://the-trivia-api.com/api/questions?diffculty={difficulty}&categories={category}&limit={count}")
    quiz = response.json()
    scores = {}
    for i in range(count):
        try:
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
            if i == 0:
                    message = await ctx.respond(f"> **{question}**", components=view)
            else:
                message = await ctx.get_channel().send(f"> **{question}**", components=view)

            await view.start(message)  # Start listening for interactions

            await view.wait()  # Wait until the view is stopped or times out

            for i in view.children:
                i.disabled=True

            await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

            if hasattr(view, "answer"):  # Check if there is an answer
                if view.answer == answer:
                    if f"{view.author}" not in scores:
                        scores[f"{view.author}"] = 1
                    else:
                        scores[f"{view.author}"] += 1
                    await ctx.get_channel().send(f"{answer} is the correct answer!")
                else:
                    if f"{view.author}" not in scores:
                            scores[f"{view.author}"] = 0
                    await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
            else:
                await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.")
        except:
            if i == 0:
                await ctx.respond("One or more of the answers was too long for the buttons. No one was awarded a point.")
            else:
                await ctx.respond("One or more of the answers was too long for the buttons. No one was awarded a point.")
    if count > 1:
        results = ""
        for i in scores:
            username = await ctx.bot.rest.fetch_user(i)
            results = results +  str(username) + " - " + str(scores[i]) + "\n"
        embed = hikari.Embed(title="Final Scores", description=f"{results}")
        await ctx.get_channel().send(embed=embed)
    else:
        username = await ctx.bot.rest.fetch_user(view.author)
        username = str(username)
        await ctx.get_channel().send(f"{username} has won!")

async def fq(ctx, count, options):
    options = options or 4
    response = requests.get(f"https://shadify.dev/api/countries/country-quiz?amount={count}&variants={options}")
    quiz = response.json()
    if count == 1:
        answer = quiz["answer"]
        flag = quiz["flag"]
        view = miru.View(timeout=60)  # Create a new view
        for j in range(options):
            view.add_item(optButtons(quiz["variants"][j], style=hikari.ButtonStyle.PRIMARY, label=quiz["variants"][j]))
        embed = hikari.Embed(title="Guess the country")
        embed.set_image(flag)
        message = await ctx.respond(embed=embed, components=view)

        await view.start(message)  # Start listening for interactions

        await view.wait()  # Wait until the view is stopped or times out

        for i in view.children:
            i.disabled=True

        await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

        if hasattr(view, "answer"):  # Check if there is an answer
            if view.answer == answer:
                await ctx.respond(f"{answer} is the correct answer!")
                username = await ctx.bot.rest.fetch_user(view.author)
                username = str(username)
                await ctx.get_channel().send(f"{username} has won!")
            else:
                await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.\nNo one won :(")
        else:
            await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.\nNo one won :(")
    else:
        scores = {}
        for i in range(count):
            answer = quiz[i]["answer"]
            flag = quiz[i]["flag"]
            view = miru.View(timeout=60)  # Create a new view
            for j in range(options):
                view.add_item(optButtons(quiz[i]["variants"][j], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["variants"][j]))
            embed = hikari.Embed(title="Guess the country")
            embed.set_image(flag)
            if i == 0:
                message = await ctx.respond(embed=embed, components=view)
            else:
                message = await ctx.get_channel().send(embed=embed, components=view)

            await view.start(message)  # Start listening for interactions

            await view.wait()  # Wait until the view is stopped or times out

            for i in view.children:
                i.disabled=True

            await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

            if hasattr(view, "answer"):  # Check if there is an answer
                if view.answer == answer:
                    if f"{view.author}" not in scores:
                        scores[f"{view.author}"] = 1
                    else:
                        scores[f"{view.author}"] += 1
                    await ctx.get_channel().send(f"{answer} is the correct answer!")
                else:
                    if f"{view.author}" not in scores:
                        scores[f"{view.author}"] = 0
                    await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
            else:
                await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.")
        results = ""
        for i in scores:
            username = await ctx.bot.rest.fetch_user(i)
            results = results +  str(username) + " - " + str(scores[i]) + "\n"
        embed = hikari.Embed(title="Final Scores", description=f"{results}")
        await ctx.get_channel().send(embed=embed)

async def cq(ctx, count, options):
    options = options or 4
    response = requests.get(f"https://shadify.dev/api/countries/capital-quiz?amount={count}&variants={options}")
    quiz = response.json()
    if count == 1:
        answer = quiz["answer"]
        flag = quiz["flag"]
        country = quiz["country"]
        view = miru.View(timeout=60)  # Create a new view
        for j in range(options):
            view.add_item(optButtons(quiz["variants"][j], style=hikari.ButtonStyle.PRIMARY, label=quiz["variants"][j]))
        embed = hikari.Embed(title=f"Guess the capital of {country}")
        embed.set_image(flag)
        message = await ctx.respond(embed=embed, components=view)

        await view.start(message)  # Start listening for interactions

        await view.wait()  # Wait until the view is stopped or times out

        for i in view.children:
            i.disabled=True

        await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

        if hasattr(view, "answer"):  # Check if there is an answer
            if view.answer == answer:
                username = await ctx.bot.rest.fetch_user(view.author)
                username = str(username)
                await ctx.get_channel().send(f"{answer} is the correct answer!\n{username} has won!")
            else:
                await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.\nNo one won :(")
        else:
            await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.\nNo one won :(")
    else:
        scores = {}
        for i in range(count):
            answer = quiz[i]["answer"]
            flag = quiz[i]["flag"]
            country = quiz[i]["country"]
            view = miru.View(timeout=60)  # Create a new view
            for j in range(options):
                view.add_item(optButtons(quiz[i]["variants"][j], style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["variants"][j]))
            embed = hikari.Embed(title=f"Guess the capital of {country}")
            embed.set_image(flag)
            if i == 0:
                message = await ctx.respond(embed=embed, components=view)
            else:
                message = await ctx.get_channel().send(embed=embed, components=view)

            await view.start(message)  # Start listening for interactions

            await view.wait()  # Wait until the view is stopped or times out

            for i in view.children:
                i.disabled=True

            await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

            if hasattr(view, "answer"):  # Check if there is an answer
                if view.answer == answer:
                    if f"{view.author}" not in scores:
                        scores[f"{view.author}"] = 1
                    else:
                        scores[f"{view.author}"] += 1
                    await ctx.get_channel().send(f"{answer} is the correct answer!")
                else:
                    if f"{view.author}" not in scores:
                        scores[f"{view.author}"] = 0
                    await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
            else:
                await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.")
        results = ""
        for i in scores:
            username = await ctx.bot.rest.fetch_user(i)
            results = results +  str(username) + " - " + str(scores[i]) + "\n"
        embed = hikari.Embed(title="Final Scores", description=f"{results}")
        await ctx.get_channel().send(embed=embed)

def load(bot):
    bot.add_plugin(plugin)