# geo-escape-bot
*For Puzzle project in Foundations of Game Design*

Play a cooperative scavenger hunt game over Discord.
 - Player 1 - Wakes up with amnesia, locked in a room. They can send messages to Player 2, but their phone is acting strange and is losing battery. Each clue solved jogs Player 1's memory of what happened the day before and can send Player 2 hints on where to go next.
 - Player 2 - Trying to find location of Player 1 by retracing their steps through hazy memories.

**How to play**
- Discord bot is hosted on Repl.it web server. Visit https://replit.com/@zajacje/geo-escape-bot#main.py and run. Add bot to server. Update CHANNEL_ID with Discord channel to play in. 
- 2 users react to welcome message to choose role (Player 1 or Player 2)
- Player 1 is DM'd with a clue/memory fragment. They must give hints to Player 2 on where to go next using a limited number of words. Messages that are too long get deleted.
- Player 2 will try to determine the location and walk there. They must type in the channel the missing word to complete the memory.
- Each message exchanged in the play channel decrements Player 1's battery life. Once the battery reaches 0, the game is over. Try to find Player 1 before battery runs out!
- If all clues are solved, congrats! You win!

**Files**

main.py
 - Runs the game. Configure game with constants at the top.


clues.py
 - Stored as a list of tuples representing (clue, answer). The clues are presented in order. The next clue is given after the current clue is answered.
  
**TO DO**
- Use PLAYING to end the game when battery ends. Can play multiple rounds without resetting bot?
