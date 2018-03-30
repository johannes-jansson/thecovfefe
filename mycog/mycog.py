import discord
import random
from discord.ext import commands

spies = {
    "5": 2,
    "6": 2,
    "7": 3,
    "8": 3,
    "9": 3,
    "10": 4
}
twofails = [7, 8, 9, 10]

class Mycog:
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}
        self.settings["Players"] = {}

    @commands.command(pass_context=True)
    async def init(self, ctx):
        server = ctx.message.server
        user = ctx.message.author
        ids = [
            "281455618559049730", # Davv_d
            "312534277524946945", # Janzon
            "217291426155855882", # Frulck
            "426671139851468810"  # Erik
        ]
        for id in ids:
            self._add_player(server.get_member(id))
        await self.bot.say("initialized")

    @commands.command()
    async def add_player(self, user : discord.Member):
        self._add_player(user)
        await self.bot.say("Added " + user.mention + " to the game.")

    def _add_player(self, user : discord.Member):
        print(user)
        print(user.id)
        print(user.name)
        print(user.mention)
        self.settings["Players"][user.id] = {"Name": user.name,
                                             "Mention": user.mention}

    @commands.command()
    async def list_players(self):
        await self.bot.say(self.settings["Players"])

    @commands.command()
    async def select_random_player(self):
        player = self._select_random_player()
        await self.bot.say(self.settings["Players"][player]["Mention"])

    def _select_random_player(self):
        players = list(self.settings["Players"].keys())
        player = random.choice(players)
        return player


def setup(bot):
    bot.add_cog(Mycog(bot))
