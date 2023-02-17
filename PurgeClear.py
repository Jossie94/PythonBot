import discord
import os
import random
from discord_components import DiscordComponents
#from dotenv import load_dotenv
from discord.ext import commands

# from bot import Fun_commands

#load_dotenv()


# Fun_commands(commands.bot)


# class trollcommands():


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    client = discord.ext.commands.Bot("!")
    DiscordComponents(client)

   # @client.event
   # async def on_ready(self):
     #   print("The command bot is online")

    @commands.command(name='hello', aliases=['hi'], pass_context=True)
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}")

    @commands.command()
    async def helpcarla(self, ctx):
        embeds = discord.Embed(title="Commands",
                               description="Carlas commands",
                               color=discord.Color.blue())
        embeds.add_field(name="!hello", value="Answers back with your discord name")
        embeds.add_field(name="!purge x", value="Delete bulk of messages. Only officers can use it/have admin rights")
        embeds.add_field(name="!hru", value="Random answers back from bot", inline=False)
        embeds.add_field(name="!timestamp or !raid <yyyy-mm-dd hh:mm>",
                         value="Registers date, time and gives choice of raid and tier")
        embeds.add_field(name="!8ball <question>", value="You ask preferably a yes or no question. Carla answer back")

        await ctx.send(embed=embeds)

    @commands.command()
    async def hru(self, ctx):
        ra = ["I am good, thank you for asking",
              "I am well. You, however, look unwell. Go outside.", "I was okay until I saw your outfit. Nasty.",
              "I might be a bot, but I am not interested.",
              "I was good until you asked. But you are not important enough to hate. Sit down.",
              "Why on earth would you ask a bot how's it doing?",
              "How am I? Who are you?"]
        await ctx.send(random.choice(ra))

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question):
        resp = ["Definitely",
                "No.",
                "Yes.",
                "What kind of question is that?",
                "Are you sure you want the answer to that?",
                "Thats not a pretty face enough for me to make me answer your question",
                "Maybe.",
                "Absolutely not",
                "Obviously",
                "Did Lethso make you ask that question? If so, its no",
                "There is this lousy bot called Carl. Ask him.",
                "Yes queen"]
        await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(resp)}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        if amount > 50:
            amount = 50
        await ctx.channel.purge(limit=amount + 1)

   # client.run(os.getenv('TOKEN'))


def setup(bot):
    bot.add_cog(FunCog(bot))
    print("loaded fun cog")

# bot.command(trollcommands(bot))
