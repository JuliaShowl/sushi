import lightbulb
import hikari
import miru
import requests

plugin = lightbulb.Plugin("flag")
plugin.add_checks(
    lightbulb.guild_only
)

class optButtons(miru.Button):
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

@plugin.command
@lightbulb.option("count", "Number of quizzes to generate (1-20) Default 1", type=int, min_value=1, max_value=20,default=1, required=False)
@lightbulb.option("options", "Number of answers to generate (2-6) Default 4", type=int, min_value=2, max_value=6, default=4, required=False)
@lightbulb.command("cq", "Capital quiz", pass_options=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def capital(ctx: lightbulb.Context, count: int, options: int):
    response = requests.get(f"https://shadify.dev/api/countries/capital-quiz?amount={count}&variants={options}")
    quiz = response.json()
    if count == 1:
        answer = quiz["answer"]
        flag = quiz["flag"]
        country = quiz["country"]
        view = miru.View(timeout=60)  # Create a new view
        for j in range(options):
            view.add_item(optButtons(quiz["variants"][j], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz["variants"][j]))
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
                await ctx.get_channel().send(f"{answer} is the correct answer!")
            else:
                await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
        else:
            await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.")
    else:
        score = 0
        for i in range(count):
            answer = quiz[i]["answer"]
            flag = quiz[i]["flag"]
            country = quiz[i]["country"]
            view = miru.View(timeout=60)  # Create a new view
            for j in range(options):
                view.add_item(optButtons(quiz[i]["variants"][j], ctx.author.id, style=hikari.ButtonStyle.PRIMARY, label=quiz[i]["variants"][j]))
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
                    score += 1
                    await ctx.get_channel().send(f"{answer} is the correct answer!")
                else:
                    await ctx.get_channel().send(f"{view.answer} is not the correct answer. The correct answer is {answer}.")
            else:
                await ctx.get_channel().send(f"Did not receive an answer in time! The correct answer is {answer}.")
        await ctx.get_channel().send(f"Total score: **{score}/{count}**")

def load(bot):
    bot.add_plugin(plugin)