import discord
import random
from discord.ext import commands

spies = {}
spies["5"] = 2
spies["6"] = 2
spies["7"] = 3
spies["8"] = 3
spies["9"] = 3
spies["10"] = 4
twofails = [7, 8, 9, 10]

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = {}
        self.settings["Players"] = {}

    @commands.command()
    async def init(self):
        self.settings["Players"]["<@312534277524946945>"] = {"Name": user.name,
                                                             "Mention": user.mention}
        await self.bot.say("initialized")

    @commands.command()
    async def mycom(self):
        await self.bot.say("I can do stuff!")

    @commands.command()
    async def add_player(self, user : discord.Member):
        print(user)
        print(user.id)
        print(user.name)
        print(user.mention)
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