import discord
import random
from discord.ext import commands

nbrOfSpies_vs_players = {
    "4": 2, # this one is just temporary
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
        self.settings["Spies"] = {}
        self.settings["Innocents"] = {}

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
    async def list_innocents(self):
        await self.bot.say(self.settings["Innocents"])

    @commands.command()
    async def list_spies(self):
        await self.bot.say(self.settings["Spies"])

    @commands.command(pass_context=True)
    async def select_spies(self, ctx):
        server = ctx.message.server
        user = ctx.message.author

        print("Started select_spies")
        spies = []
        innocents = self.settings["Players"].copy()
        print(innocents)
        print(nbrOfSpies_vs_players)
        nbrOfSpies = nbrOfSpies_vs_players[str(len(innocents))]
        print(nbrOfSpies)
        for i in range(nbrOfSpies):
            spy = random.choice(list(innocents.keys()))
            innocents.pop(spy)
            spies.append(server.get_member(spy))
        self.settings["Innocents"] = innocents
        for spy in spies:
            self.settings["Spies"][spy.id] = {"Name": spy.name,
                                              "Mention": spy.mention}
        await self.bot.say("The spies have been selected")

    @commands.command(pass_context=True)
    async def startvote(self, ctx):
        server = ctx.message.server
        # voters = self.settings["Spies"]
        # for voter in voters:
        #     self._request_vote(ctx, voter)
        await self._request_vote(ctx, server.get_member("312534277524946945"))

    async def _request_vote(self, ctx, user):
        await self.bot.send_message(user, "Suggested team is ---. Yes or no? (y/n)")
        channel = await self.bot.start_private_message(user)
        r = (await self.bot.wait_for_message(channel=channel,author=user))
        print(r.content)
        if r.content == "y" or r.content == "yes":
            await self.bot.say("Somebody voted yes")
        elif r.content == "n" or r.content == "no":
            await self.bot.say("Somebody voted no")
        else:
            await self.bot.say("Somebody provided an invalid vote - that counts as a no")
        # await self.bot.say(r.content)


    @commands.command(pass_context=True)
    async def send_roles(self, ctx):
        server = ctx.message.server
        print("Evils:")
        for id in list(self.settings["Spies"].keys()):
            # user = server.get_member("312534277524946945")
            user = server.get_member(id)
            await self.bot.send_message(user, "Oh no, you're a spy!")
        print("Innocents:")
        for id in list(self.settings["Innocents"].keys()):
            user = server.get_member(id)
            await self.bot.send_message(user, "Your concience is clear - you're innocent")



def setup(bot):
    bot.add_cog(Mycog(bot))

if __name__ == '__main__':
    mycog = Mycog()
    mycog.init()
    mycog.select_spies()
