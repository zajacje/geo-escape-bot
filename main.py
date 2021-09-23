import discord
import os

from clues import clues

# Connect to discord
client = discord.Client()

# Configure game
PLAYER1_ID = 0 # ID of user stuck in room receiving clues
PLAYER2_ID = 0 # ID of user walking around
CHANNEL_ID = 890313505981493258 # Channel ID where game is being played
battery = 100 # Starting %
BATTERY_DEC = 10 # Each message decreases battery by this %
MAX_HINT_LEN = 2 # How many words are allowed in hint
NO_BATTERY_MSG = "Your phone ran out of battery :(" # Display when no more battery
WIN_MSG = 'Congratulations!' # Display when won (solved all clues)
EMOJI_1 = '1️⃣'
EMOJI_2 = '2️⃣'
WELCOME_MSG = 'Welcome. Which player are you?\n ' + EMOJI_1 + ' -> Player 1\n ' + EMOJI_2 + ' -> Player 2\nPlease enter answers in all lowercase. Be careful, your phone has limited battery...'

# Initialize variables
clue = ''
answer = ''
PLAYING = True

# Gets the next clue in the from the queue. Updates clue and answer
def get_next_clue():
  global clue 
  global answer

  pair = clues.get()
  clue = pair[0]
  answer = pair[1]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

  # Start the game
  channel = client.get_channel(int(CHANNEL_ID))
  init_msg = await channel.send(WELCOME_MSG)
  await init_msg.add_reaction(EMOJI_1)
  await init_msg.add_reaction(EMOJI_2)

  # Starting battery
  channel = client.get_channel(int(CHANNEL_ID))
  await channel.send("Battery level: " + str(battery))

# Set player 1 and player 2  
@client.event
async def on_reaction_add(reaction, user):
  # Ignore messages from ourselves, do nothing
  if user == client.user:
    return
  
  global PLAYER1_ID
  global PLAYER2_ID

  # Player 1: set playerID and send 1st clue
  if reaction.emoji == EMOJI_1:
    PLAYER1_ID = user.id
    get_next_clue()
    user = await client.fetch_user(int(PLAYER1_ID))
    await user.send(clue)
    await user.send('INSERT MESSAGE HERE. Your phone seems buggy and won\'t send messages more than ' + str(MAX_HINT_LEN) + ' words long!')
    print('Set player 1: ' + str(user.name))
  
  # Player 2: set playerID
  if reaction.emoji == EMOJI_2:
    PLAYER2_ID = user.id
    print('Set player 2: ' + str(user.name))

# Receives message and responds
@client.event
async def on_message(message):
  # If message if sent from ourselves, do nothing
  if message.author == client.user:
      return

  # Get users and channel
  player1 = await client.fetch_user(int(PLAYER1_ID))
  player2 = await client.fetch_user(int(PLAYER2_ID))
  channel = client.get_channel(int(CHANNEL_ID))

  # Check player1's messages
  if message.author == player1 and message.channel == channel:
    hint = message.content.split(" ")

    # Allow only hints within MAX_HINT_LENGTH
    if len(hint) > MAX_HINT_LEN:
      await message.delete()
      await player1.send("Message failed to send. Due to a bug in your phone, you can only send messages with <= " + str(MAX_HINT_LEN) + " words. Your message had " + str(len(hint)) + " words.");
      return

  # Update battery
  global PLAYING
  if PLAYING and message.channel == channel:
    global battery
    battery -= BATTERY_DEC
    #channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Battery level: " + str(battery))

  # Check if no more battery
  if battery == 0:
    print("NO BATTERY LEFT")
    #user = await client.fetch_user(int(PLAYER1_ID))
    #await user.send(NO_BATTERY_MSG)
    channel.send(NO_BATTERY_MSG)
    PLAYING = False

  # Check player2's messages
  if message.author == player2 and message.channel == channel:
    # Check if won
    if message.content == answer:
      if clues.empty():
        PLAYING = False
        #channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(WIN_MSG)

      # Send next clue
      else:
        print("SOLVED: " + clue)
        get_next_clue()
        #user = await client.fetch_user(int(PLAYER1_ID))
        #await user.send(clue)
        await player1.send(clue)


# Run bot with token
client.run(os.getenv('TOKEN'))

