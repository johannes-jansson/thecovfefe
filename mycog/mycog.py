import discord
import random
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = {}
        self.settings["Players"] = {}

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")

    @commands.command()
    async def add_player(self, user : discord.Member):
        self.settings["Players"][user.id] = {"Name": user.name,
                                             "Mention": user.mention}
        await self.bot.say("Added " + user.mention + " to the game.")

    @commands.command()
    async def list_players(self):
        await self.bot.say(self.settings["Players"])

    @commands.command()
    async def select_random_player(self):
        players = list(self.settings["Players"].keys())
        player = random.choice(players)
        await self.bot.say(self.settings["Players"][player]["Mention"])


def setup(bot):
    bot.add_cog(Mycog(bot))
