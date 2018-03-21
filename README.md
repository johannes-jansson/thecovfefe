# thecovfefe
A discord bot for playing the amazing deception game The Covfefe (inspired by [The Resistance](https://en.wikipedia.org/wiki/The_Resistance_(game)))

## How a game could look like

`covfefestart` should start a game with all members of the current channel. Every player should recieve a message with the text "Congrats! You are a russian sympathizer" if they are innocent, or "Oh no! You are an american patriot, together with NN and NN" if they are not.

All players should be shuffeled into a play order, that should be displayed with an arrow pointing to the current leader player.

`covfefenominate NN, NN` can only be invoked by the current leader. Whenever called, it initiates a semi-closed vote.

`covfefevote y/yes/n/no` can be called once by each player. When this is done by all players, the results are displayed. If the vote fails, next player becomes leader and the failcounter is increased by one. If the vote passes, the failcounter is reset and the nominated players get to do a closed vote. 

`covfefevote p/pass/f/fail` will have to be called by all nominated players. Innocent players can vote whatever they want, it will still be interpreted as a pass. Other players votes actually matter. If all votes (or all but 1) are pass, this is displayed. If not, this is displayed. The "scoreboard" is updated, and the next round begins. 

## Links for inspiration

- https://github.com/Cog-Creators/Red-DiscordBot - the bot we will probably base this project on
- http://theresistanceplus.com/ - web implementation
- http://playavalononline.com/ - web implementation
