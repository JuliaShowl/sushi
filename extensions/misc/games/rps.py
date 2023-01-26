import lightbulb
import hikari
import miru
import random

plugin = lightbulb.Plugin("rps")
plugin.add_checks(
    lightbulb.guild_only
)

class optButtons(miru.Button):
    def __init__(self, choice, author, players, *args, **kwargs) -> None:
        self.choice = choice
        self.author = author
        self.players = players
        super().__init__(*args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        if self.players == 1:
            if ctx.user.id == self.author:
                self.view.answer = self.choice
                self.view.stop()
            else:
                await ctx.respond("You did not generate this game", flags=hikari.MessageFlag.EPHEMERAL)
        else:
            self.view.answer = self.choice
            self.view.author = self.author
            self.view.stop()


class challengeButton(miru.Button):
    def __init__(self, choice, challenger, *args, **kwargs) -> None:
        self.choice = choice
        self.challenger = challenger
        super().__init__(*args, **kwargs)

    async def callback(self, ctx: miru.ViewContext) -> None:
        if ctx.user.id == self.challenger:
            self.view.answer = self.choice
            self.view.stop()
        else:
            await ctx.respond("You were not challenged.", flags=hikari.MessageFlag.EPHEMERAL)

@plugin.command
@lightbulb.option("user", "Specifically challenge another user", type=hikari.User, required=False)
@lightbulb.option("players", "Play against a computer or against each other. Default single player if not challenging a user", type=int, min_value=1, max_value=2, default=1, required=False)
@lightbulb.command("rps", "Rock, paper, scissors", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context, players: int, user: hikari.User):
    if user is not None:
        challenge = miru.View(timeout=60)  # Create a new view
        challenge.add_item(challengeButton("Yes", user.id, style=hikari.ButtonStyle.SUCCESS, label="Accept"))
        challenge.add_item(challengeButton("No", user.id, style=hikari.ButtonStyle.DANGER, label="Decline"))
        message = await ctx.respond(f"{ctx.author.mention} is challenging {user.mention} to RPS!", components=challenge, user_mentions=True)

        await challenge.start(message)  # Start listening for interactions

        await challenge.wait()  # Wait until the view is stopped or times out

        for i in challenge.children:
            i.disabled=True

        await message.edit(components=challenge.build()) # Disable all buttons after view is stopped or times out

        if hasattr(challenge, "answer"):
            if(challenge.answer == "No"):
                await ctx.get_channel().send(f"{user.mention} has denied your request for RPS.")
                return
            else:
                p1view = miru.View(timeout=60)  # Create a new view
                p1view.add_item(optButtons("Rock", ctx.author.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Rock"))
                p1view.add_item(optButtons("Paper", ctx.author.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Paper"))
                p1view.add_item(optButtons("Scissors", ctx.author.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Scissors"))
                message = await ctx.respond(f"{ctx.author.mention}'s move", components=p1view)

                await p1view.start(message)  # Start listening for interactions

                await p1view.wait()  # Wait until the view is stopped or times out

                for i in p1view.children:
                    i.disabled=True

                await message.edit(components=p1view.build()) # Disable all buttons after view is stopped or times out
                
                p1 = p1view.answer

                p2view = miru.View(timeout=60)  # Create a new view
                p2view.add_item(optButtons("Rock", user.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Rock"))
                p2view.add_item(optButtons("Paper", user.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Paper"))
                p2view.add_item(optButtons("Scissors", user.id, 1, style=hikari.ButtonStyle.PRIMARY, label="Scissors"))
                message = await ctx.get_channel().send(f"{user.mention}'s move", components=p2view)

                await p2view.start(message)  # Start listening for interactions

                await p2view.wait()  # Wait until the view is stopped or times out

                for i in p2view.children:
                    i.disabled=True

                await message.edit(components=p2view.build()) # Disable all buttons after view is stopped or times out

                p2 = p2view.answer

                if hasattr(p1view, "answer") and hasattr(p2view, "answer"):  # Check if there is an answer
                    if p1 == "Rock" and p2 == "Scissors" or p1 == "Paper" and p2 == "Rock" or p1 == "Scissors" and p2 == "Paper":
                        await ctx.get_channel().send(f"{ctx.author.mention}'s {p1} beats {user.mention}'s {p2}.")
                    elif p2 == "Rock" and p1 == "Scissors" or p2 == "Paper" and p1 == "Rock" or p2 == "Scissors" and p1 == "Paper":
                        await ctx.get_channel().send(f"{user.mention}'s {p2} beats {ctx.author.mention}'s {p1}.")
                    else:
                        await ctx.get_channel().send(f"Both players chose {p1}")
                else:
                    await ctx.get_channel().send(f"Did not receive an answer in time!")
        else:
            await ctx.respond(f"Did not receive an answer in time!")
    elif players == 1:
        view = miru.View(timeout=60)  # Create a new view
        view.add_item(optButtons("Rock", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Rock"))
        view.add_item(optButtons("Paper", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Paper"))
        view.add_item(optButtons("Scissors", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Scissors"))
        message = await ctx.respond(f"{ctx.author.mention}'s move", components=view)

        await view.start(message)  # Start listening for interactions

        await view.wait()  # Wait until the view is stopped or times out

        for i in view.children:
            i.disabled=True

        await message.edit(components=view.build()) # Disable all buttons after view is stopped or times out

        bot = ""
        # generate random move
        comp = random.randint(1,3)
        if comp == 1:
            bot = "Rock"
        elif comp == 2:
            bot = "Paper"
        else:
            bot = "Scissors"

        await ctx.get_channel().send(f"Sushi chose {bot}.")
        
        if hasattr(view, "answer"):  # Check if there is an answer
            if view.answer == "Rock" and bot == "Scissors" or view.answer == "Paper" and bot == "Rock" or view.answer == "Scissors" and bot == "Paper":
                await ctx.get_channel().send(f"{ctx.author.mention}'s {view.answer} beats Sushi's {bot}.")
            elif bot == "Rock" and view.answer == "Scissors" or bot == "Paper" and view.answer == "Rock" or bot == "Scissors" and view.answer == "Paper":
                await ctx.get_channel().send(f"Sushi's {bot} beats {ctx.author.mention}'s {view.answer}.")
            else:
                await ctx.get_channel().send(f"Both players chose {bot}")
        else:
            await ctx.respond(f"Did not receive an answer in time!")
    
    else:
        p1view = miru.View(timeout=60)  # Create a new view
        p1view.add_item(optButtons("Rock", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Rock"))
        p1view.add_item(optButtons("Paper", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Paper"))
        p1view.add_item(optButtons("Scissors", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Scissors"))
        message = await ctx.respond(f"{ctx.author.mention}'s move", components=p1view)

        await p1view.start(message)  # Start listening for interactions

        await p1view.wait()  # Wait until the view is stopped or times out

        for i in p1view.children:
            i.disabled=True

        await message.edit(components=p1view.build()) # Disable all buttons after view is stopped or times out

        p1 = p1view.answer

        p2view = miru.View(timeout=60)  # Create a new view
        p2view.add_item(optButtons("Rock", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Rock"))
        p2view.add_item(optButtons("Paper", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Paper"))
        p2view.add_item(optButtons("Scissors", ctx.author.id, players, style=hikari.ButtonStyle.PRIMARY, label="Scissors"))
        message = await ctx.get_channel().send(f"Player 2's move", components=p2view)

        await p2view.start(message)  # Start listening for interactions

        await p2view.wait()  # Wait until the view is stopped or times out

        for i in p2view.children:
            i.disabled=True

        await message.edit(components=p2view.build()) # Disable all buttons after view is stopped or times out

        p2 = p2view.answer
        p2User = await ctx.bot.rest.fetch_user(p2view.author)

        if hasattr(p1view, "answer") and hasattr(p2view, "answer"):  # Check if there is an answer
            if p1 == "Rock" and p2 == "Scissors" or p1 == "Paper" and p2 == "Rock" or p1 == "Scissors" and p2 == "Paper":
                await ctx.get_channel().send(f"{ctx.author.mention}'s {p1} beats {p2User.mention}'s {p2}.")
            elif p2 == "Rock" and p1 == "Scissors" or p2 == "Paper" and p1 == "Rock" or p2 == "Scissors" and p1 == "Paper":
                await ctx.get_channel().send(f"{p2User.mention}'s {p2} beats {ctx.author.mention}'s {p1}.")
            else:
                await ctx.get_channel().send(f"Both players chose {p1}")
        else:
            await ctx.respond(f"Did not receive an answer in time!")


def load(bot):
    bot.add_plugin(plugin)