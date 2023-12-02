## Start Game

```
python main.py
```


1. Board Setup: The congkak board typically consists of two rows of seven small holes (also known as 'houses') and two larger holes at the ends (known as 'stores' or 'home'). At the start of the game, seven game pieces (usually small seeds, shells, or marbles) are placed in each of the fourteen smaller holes. The larger holes (stores) are left empty.

2. Turns: Unlike traditional Congkak, in this version, both players start playing simultaneously. A turn consists of choosing one of the holes on their side of the board and 'sowing' the seeds — this means picking up all the seeds in the chosen hole and distributing them one by one into the following holes in a counter-clockwise direction.

3. Sowing Rules: When sowing, if the last seed lands in a non-empty house on either player's side, the player collects all the seeds from that house and continues sowing. If the last seed lands in the player's own store, they continue with another turn. If the last seed lands in an empty house on the player's own side, the turn ends. 

4. Capturing: If the last seed sown lands in an empty house on the player's own side, and if there are seeds in the opponent's house directly opposite, all the seeds in the opponent's house are 'captured' and placed in the player's store. The turn then ends.

5. End of the Game: The game ends when all the houses on one side of the board are empty. The player who still has seeds on their side of the board puts all remaining seeds into their store. The player with the most seeds in their store at the end of the game is the winner.

Note: Since players start simultaneously, there may be instances where both players reach for the same house (the middle one) at the same time. You may want to add a rule to handle this situation, for instance, giving priority to a certain player, or making it a 'dead zone' where no one can play until it's the only option left.
