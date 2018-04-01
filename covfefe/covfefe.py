import discord
import random
from random import shuffle
from .utils.dataIO import dataIO
from discord.ext import commands

innocentmessages = [
    "Your concience is clear - you're a good ole' russian infiltrator! :flag_ru:"
]
spymessages = [
    "Oh no, you're an american patriot! What are you doing in the oval office?! :flag_us:"
]

numberEmojis = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:"]
nbrOfSpies_vs_players = {
    "2": 1, # this one is just temporary
    "5": 2,
    "6": 2,
    "7": 3,
    "8": 3,
    "9": 3,
    "10": 4
}
twofails = [7, 8, 9, 10]

missions = {
    "2" : [1,1,1,1,1],
    "5" : [2,3,2,3,3],
    "6" : [2,3,4,3,4],
    "7" : [2,3,3,4,4],
    "8" : [3,4,4,5,5],
    "9" : [3,4,4,5,5],
    "10": [3,4,4,5,5]
}

class Covfefe:
    def __init__(self, bot):
        print("")
        print("")
        print("")
        self.bot = bot

    @commands.command(pass_context=True)
    async def start(self, ctx, options: str):
        await self._start(ctx, options)

    async def _start(self, ctx, options: str):
        server = ctx.message.server
        self.settings = {} # reset
        self.settings["Players"] = {}
        self.settings["playerOrder"] = []
        self.settings["currentPlayer"] = 0
        self.settings["Spies"] = {}
        self.settings["Innocents"] = {}
        self.settings["voteTrackCounter"] = 0
        self.settings["missionCounter"] = 0
        self.settings["missionResults"] = [] # append booleans

        players = []
        for player in options.replace(" ", "").split(","):
            self._add_player(server.get_member(player[2:-1]))
            self.settings["playerOrder"].append(server.get_member(player[2:-1]))
        shuffle(self.settings["playerOrder"])
        await self._select_spies(ctx)
        await self._send_roles(ctx)
        await self._display_scoreboard(ctx)
        await self._display_player_order(ctx)
        await self._notify_leader(ctx)

    @commands.command(pass_context=True)
    async def notify_leader(self, ctx):
        await self._notify_leader(ctx)

    async def _notify_leader(self, ctx):
        server = ctx.message.server
        leader = self.settings["playerOrder"][self.settings["currentPlayer"]].mention
        players = missions[str(len(self.settings["Players"]))][self.settings["missionCounter"]]
        await self.bot.say(leader + ", it's your turn to nominate a team! Nominate " + str(players) + " players to go on a mission by writing `covfefenominate \"@player1 , @player2 \"` but with the actual players you want to nominate.")

    @commands.command(pass_context=True)
    async def display_scoreboard(self, ctx):
        await self._display_scoreboard(ctx)

    async def _display_scoreboard(self, ctx):
        server = ctx.message.server
        outstring = "Scoreboard:\n"
        for i in range(self.settings["missionCounter"]):
            if self.settings["missionResults"][i]:
                outstring = outstring + ":flag_ru:" + " "
            else:
                outstring = outstring + ":flag_us:" + " "
        for i in range(self.settings["missionCounter"], 5):
            outstring = outstring + numberEmojis[missions[str(len(self.settings["Players"]))][i]] + " "

        outstring = outstring + "\n\nVote track: " + str(self.settings["voteTrackCounter"]) + "/5 tries\n\n" + str(len(self.settings["Players"])) + " players, " + str(len(self.settings["Spies"])) + " spies\n\n"
        await self.bot.say(outstring)

    @commands.command(pass_context=True)
    async def display_player_order(self, ctx):
        await self._display_player_order(ctx)

    async def _display_player_order(self, ctx):
        server = ctx.message.server
        players = self.settings["playerOrder"]
        await self.bot.say("Players: ")
        for player in players:
            playerName = server.get_member(player.id).name
            if players.index(player) == self.settings["currentPlayer"]:
                await self.bot.say(str(players.index(player) + 1) + ". " + playerName + " <-")
            else:
                await self.bot.say(str(players.index(player) + 1) + ". " + playerName)

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
        await self._select_spies(ctx)

    async def _select_spies(self, ctx):
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
        await self._send_roles(ctx)

    async def _send_roles(self, ctx):
        print("")
        print("### send roles")
        server = ctx.message.server
        spies = list(self.settings["Spies"].keys())
        print(spies)
        print("Evils:")
        for id in list(self.settings["Spies"].keys()):
            # user = server.get_member("312534277524946945")
            user = server.get_member(id)
            outstring = random.choice(spymessages) + "\n"
            outstring = outstring + "Patriots this round are:\n"
            for spy in spies:
                outstring = outstring + server.get_member(spy).mention + "\n"
            await self.bot.send_message(user, outstring)
        print("Innocents:")
        for id in list(self.settings["Innocents"].keys()):
            user = server.get_member(id)
            await self.bot.send_message(user, random.choice(innocentmessages))



def setup(bot):
    bot.add_cog(Covfefe(bot))
