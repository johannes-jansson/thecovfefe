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
    "2": 1,  # this one is just temporary
    "5": 2,
    "6": 2,
    "7": 3,
    "8": 3,
    "9": 3,
    "10": 4
}
twofails = [7, 8, 9, 10]

missions = {
    "2": [1, 1, 1, 1, 1],
    "5": [2, 3, 2, 3, 3],
    "6": [2, 3, 4, 3, 4],
    "7": [2, 3, 3, 4, 4],
    "8": [3, 4, 4, 5, 5],
    "9": [3, 4, 4, 5, 5],
    "10": [3, 4, 4, 5, 5]
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
        self.settings = {}  # reset
        self.settings["Players"] = {}
        self.settings["playerOrder"] = []
        self.settings["currentPlayer"] = 0
        self.settings["Spies"] = {}
        self.settings["Innocents"] = {}
        self.settings["vote_track_counter"] = 4
        self.settings["missionCounter"] = 0
        self.settings["missionResults"] = []  # append booleans
        self.settings["nominated"] = []
        self.settings["votingresults"] = {}
        self.settings["successvotingresults"] = {}

        for player in options.replace(" ", "").split(","):
            self._add_player(server.get_member(player[2:-1]))
            self.settings["playerOrder"].append(server.get_member(player[2:-1]))
        # shuffle(self.settings["playerOrder"])
        await self._select_spies(ctx)
        await self._send_roles(ctx)
        await self._display_scoreboard(ctx)
        await self._display_player_order(ctx)
        await self._notify_leader(ctx)

    @commands.command(pass_context=True)
    async def init(self, ctx):
        server = ctx.message.server
        user = ctx.message.author
        ids = [
            "281455618559049730",  # Davv_d
            "312534277524946945",  # Janzon
            "217291426155855882",  # Frulck
            "426671139851468810"   # Erik
        ]
        for id in ids:
            self._add_player(server.get_member(id))
        await self.bot.say("initialized")

    # PHASE ONE
    ###########
    @commands.command()
    async def add_player(self, user: discord.Member):
        self._add_player(user)
        await self.bot.say("Added " + user.mention + " to the game.")

    def _add_player(self, user: discord.Member):
        self.settings["Players"][user.id] = {"Name": user.name,
                                             "Mention": user.mention}

    @commands.command(pass_context=True)
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

        spies = []
        innocents = self.settings["Players"].copy()
        nbrOfSpies = nbrOfSpies_vs_players[str(len(innocents))]
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
    async def display_scoreboard(self, ctx):
        await self._display_scoreboard(ctx)

    async def _display_scoreboard(self, ctx):
        server = ctx.message.server
        outstring = "Scoreboard:\n\n"
        for i in range(self.settings["missionCounter"]):
            if self.settings["missionResults"][i]:
                outstring = outstring + ":flag_ru:" + " "
            else:
                outstring = outstring + ":flag_us:" + " "
        for i in range(self.settings["missionCounter"], 5):
            outstring = outstring + numberEmojis[missions[str(len(self.settings["Players"]))][i]] + " "

        outstring = outstring + "\n\nVote track: {}/5 tries\n\nPlayers: {}\nSpies: {}\n\n".format(
            self.settings["vote_track_counter"],
            len(self.settings["Players"]),
            len(self.settings["Spies"]))
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
    async def send_roles(self, ctx):
        await self._send_roles(ctx)

    async def _send_roles(self, ctx):
        server = ctx.message.server
        spies = list(self.settings["Spies"].keys())
        for id in list(self.settings["Spies"].keys()):
            # user = server.get_member("312534277524946945")
            user = server.get_member(id)
            outstring = random.choice(spymessages) + "\n"
            outstring = outstring + "Patriots this round are:\n"
            for spy in spies:
                outstring = outstring + server.get_member(spy).mention + "\n"
            await self.bot.send_message(user, outstring)
        for id in list(self.settings["Innocents"].keys()):
            user = server.get_member(id)
            await self.bot.send_message(user, random.choice(innocentmessages))

    @commands.command(pass_context=True)
    async def notify_leader(self, ctx):
        await self._notify_leader(ctx)

    async def _notify_leader(self, ctx):
        server = ctx.message.server
        leader = self.settings["playerOrder"][self.settings["currentPlayer"]].mention
        players = missions[str(len(self.settings["Players"]))][self.settings["missionCounter"]]
        await self.bot.say(leader + ", it's your turn to nominate a team! Nominate " + str(players) + " players to go on a mission by writing `covfefenominate \"@player1 , @player2 \"` but with the actual players you want to nominate.")

    @commands.command(pass_context=True)
    async def nominate(self, ctx, options: str):
        await self._nominate(ctx, options)

    async def _nominate(self, ctx, options: str):
        server = ctx.message.server
        if ctx.message.author != self.settings["playerOrder"][self.settings["currentPlayer"]]:
            await self.bot.say("You're not the game leader! " + self.settings["playerOrder"][self.settings["currentPlayer"]].mention + " must nominate a squad!")
        else:

            self.settings["nominated"] = []

            for player in options.replace(" ", "").split(","):
                self.settings["nominated"].append(server.get_member(player[2:-1]))

            try:
                if len(self.settings["nominated"]) == missions[str(len(self.settings["Players"]))][self.settings["missionCounter"]]:
                    await self._display_nominated(ctx)
                else:
                    await self.bot.say("Inncorrect number of nominees, something is sketchy here! Vote failed automatically")
            except KeyError:
                await self.bot.say("Inncorrect nomination, something is very sketchy here! Vote failed automatically")

    # PHASE TWO
    ###########
    @commands.command(pass_context=True)
    async def display_nominated(self, ctx):
        await self._display_nominated(ctx)

    async def _display_nominated(self, ctx):
        server = ctx.message.server
        players = self.settings["nominated"]
        await self.bot.say("Nominated players: ")
        for player in players:
            playerName = server.get_member(player.id).name
            await self.bot.say(str(players.index(player) + 1) + ". " + playerName)
        await self.bot.say("It's time to vote! You have recieved a private message with instructions")
        await self._send_approve_vote(ctx)

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
        r = (await self.bot.wait_for_message(channel=channel, author=user))
        if r.content == "y" or r.content == "yes":
            await self.bot.say("Somebody voted yes")
        elif r.content == "n" or r.content == "no":
            await self.bot.say("Somebody voted no")
        else:
            await self.bot.say("Somebody provided an invalid vote - that counts as a no")
        # await self.bot.say(r.content)

    @commands.command(pass_context=True)
    async def send_approve_vote(self, ctx):
        await self._send_approve_vote(ctx)

    async def _send_approve_vote(self, ctx):
        server = ctx.message.server

        for player in list(self.settings["Players"].keys()):
            user = server.get_member(player)
            outstring = "It's time to vote!\n"
            outstring = outstring + "Nominees this round are:\n"

            for nom in self.settings["nominated"]:
                player_name = server.get_member(nom.id).mention
                # outstring = outstring + server.get_member(spy).mention + "\n"
                outstring = outstring + "-" + player_name + "\n"
            outstring = outstring + "\n To approve, reply with `a`. To reject, reply with `r`"
            await self.bot.send_message(user, outstring)
        await self._wait_for_votes(ctx)

    # PHASE THREE
    #############
    @commands.command(pass_context=True)
    async def wait_for_votes(self, ctx):
        await self._wait_for_votes(ctx)

    async def _wait_for_votes(self, ctx):
        print("entered wait for votes")
        server = ctx.message.server

        for player in list(self.settings["Players"].keys()):
            user = server.get_member(player)
            if player == "389116259402252288":
                self.settings["votingresults"][user] = True
                await self._check_if_vote_complete(ctx)
                continue
            print("listening for reply from:")
            print(player)
            print(user)
            channel = await self.bot.start_private_message(user)
            answer = False
            r = (await self.bot.wait_for_message(channel=channel,
                                                 author=user))
            r = r.content.lower().strip()
            print("answer")
            print(r)
            if r == "a":
                answer = True
            elif r == "r":
                answer = False
            else:
                outstring = "Your message was neither `a` nor `r`, so I'll go ahead and interpret it as a rejection"
                await self.bot.send_message(user, outstring)
            self.settings["votingresults"][user] = answer
            await self._check_if_vote_complete(ctx)

    async def _check_if_vote_complete(self, ctx):
        if len(self.settings["votingresults"].keys()) == len(self.settings["Players"].keys()):
            print("everybody voted!")
            await self._count_votes(ctx)
        else:
            print("voting not done!")

    async def count_votes(self, ctx):
        await self._count_votes(ctx)

    async def _count_votes(self, ctx):
        server = ctx.message.server
        print("entered count votes")

        number_of_voters = len(self.settings["votingresults"].keys())
        approves = 0
        playeroutstring = ""
        for player in self.settings["votingresults"].keys():
            playeroutstring += "- " + player.mention + " voted "
            if self.settings["votingresults"][player]:
                playeroutstring += "`approve`\n"
                approves += 1
            else:
                playeroutstring += "`reject`\n"
        result_outstring = "{} voted approve, {} voted reject.\n".format(approves, number_of_voters - approves)
        # self.settings["nominated"] = []
        self.settings["votingresults"] = {}
        if approves > number_of_voters / 2:
            self.settings["vote_track_counter"] = 0
            await self.bot.say("The vote passed!\n\n" + result_outstring + playeroutstring + "\n\n")
            print("about to send success vote")
            await self._send_success_vote(ctx)
        else:
            await self.bot.say("The vote failed!\n\n" + result_outstring + playeroutstring + "\n\n")
            self.settings["vote_track_counter"] += 1
            self.update_current_player()
            if self.settings["vote_track_counter"] >= 5:
                self.settings["vote_track_counter"] = 0
                await self.bot.say("Too many failed votes, the americans automatically won this mission! :grimacing:")
                self.settings["vote_track_counter"] = 0
                self.settings["missionCounter"] += 1
                self.settings["missionResults"].append(False)

            await self._display_scoreboard(ctx)
            await self._display_player_order(ctx)
            await self._notify_leader(ctx)

    def update_current_player(self):
        self.settings["currentPlayer"] += 1
        if self.settings["currentPlayer"] >= len(self.settings["Players"].keys()):
            self.settings["currentPlayer"] = 0

    # Phase four?
    #############
    @commands.command(pass_context=True)
    async def send_success_vote(self, ctx):
        await self._send_success_vote(ctx)

    async def _send_success_vote(self, ctx):
        print("entered send success vote")
        server = ctx.message.server

        playerstring = "People on this mission:\n"
        for player in self.settings["nominated"]:
            player_name = server.get_member(player.id).mention
            playerstring += "-" + player_name + "\n"
        await self.bot.say("It's time for the nominated players to go on their mission!\n" + playerstring)

        for player in self.settings["nominated"]:
            user = server.get_member(player.id)
            outstring = "It's time to decide whether the mission should be successful!\n"

            # outstring = outstring + "People on this mission:\n"
            # for nom in self.settings["nominated"]:
            #     print("hipp")
            #     player_name = server.get_member(nom.id).mention
            #     print("happ")
            #     # outstring = outstring + server.get_member(spy).mention + "\n"
            #     outstring = outstring + "-" + player_name + "\n"

            outstring += playerstring


            outstring = outstring + "\n If you want the mission to be successful, reply with `s`. If you want the mission to fail, reply with `f`"
            if player in list(self.settings["Innocents"].keys()):
                outstring += "\n Since you're innocent your vote will count as a `success` whatever you reply."
            await self.bot.send_message(user, outstring)
        await self._wait_for_success_votes(ctx)

    @commands.command(pass_context=True)
    async def wait_for_success_votes(self, ctx):
        await self._wait_for_success_votes(ctx)

    async def _wait_for_success_votes(self, ctx):
        print("entered wait for success votes")
        server = ctx.message.server

        for player in self.settings["nominated"]:
            user = server.get_member(player.id)
            if player == "389116259402252288":
                self.settings["successvotingresults"][user] = True
                await self._check_if_success_vote_complete(ctx)
                continue
            print("listening for reply from:")
            print(player)
            print(user)
            channel = await self.bot.start_private_message(user)
            answer = True
            r = (await self.bot.wait_for_message(channel=channel,
                                                 author=user))
            r = r.content.lower().strip()
            print("answer")
            print(r)
            if r == "s":
                answer = True
            elif r == "f":
                answer = False
            else:
                outstring = "Your message was neither `a` nor `r`, so I'll go ahead and interpret it as a success"
                await self.bot.send_message(user, outstring)
            self.settings["successvotingresults"][user] = answer
            await self._check_if_success_vote_complete(ctx)

    async def _check_if_success_vote_complete(self, ctx):
        if len(self.settings["successvotingresults"].keys()) == len(self.settings["nominated"]):
            print("everybody voted!")
            await self._count_success_votes(ctx)
        else:
            print("voting not done!")

    async def count_success_votes(self, ctx):
        await self._count_success_votes(ctx)

    async def _count_success_votes(self, ctx):
        server = ctx.message.server
        print("entered count success votes")

        number_of_voters = len(self.settings["successvotingresults"].keys())
        successes = 0
        for player in self.settings["successvotingresults"].keys():
            if self.settings["successvotingresults"][player]:
                successes += 1
        result_outstring = "{} voted success, {} voted fail.\n".format(successes, number_of_voters - successes)
        self.settings["nominated"] = []
        self.settings["successvotingresults"] = {}
        self.settings["missionCounter"] += 1
        # self.update_current_player()
        if successes > number_of_voters / 2:
            await self.bot.say("The mission succeded!\n\n" + result_outstring + "\n\n")
            self.settings["missionResults"].append(True)
        else:
            await self.bot.say("The mission failed!\n\n" + result_outstring + "\n\n")
            self.settings["missionResults"].append(False)

        await self._display_scoreboard(ctx)
        await self._display_player_order(ctx)
        await self._notify_leader(ctx)


def setup(bot):
    bot.add_cog(Covfefe(bot))
