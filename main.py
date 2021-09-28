import discord
import os
import queue
from time import time, ctime

# Connect to discord
client = discord.Client()

# Configure game
PLAYER1_ID = 0  # ID of user stuck in room receiving clues
PLAYER2_ID = 0  # ID of user walking around
CHANNEL_ID = 890313505981493258  # Channel ID where game is being played
battery = 100  # Starting %
BATTERY_DEC = 2  # Each message decreases battery by this %
BATTERY_INC = 10  # When players solve a clue, it increases by this %
SMALL_BATTERY_INC = 5 # When players confirm the location
MAX_HINT_LEN = 2  # How many words are allowed in hint
NO_BATTERY_MSG = "Your phone ran out of battery 😭"  # Display when no more battery
WIN_MSG = 'Congratulations!'  # Display when won (solved all clues)
EMOJI_1 = '1️⃣'
EMOJI_2 = '2️⃣'
WELCOME_MSG = 'Welcome. Which player are you?\n ' + EMOJI_1 + ' -> Player 1\n ' + EMOJI_2 + ' -> Player 2\nPlease enter answers in all lowercase. Be careful, your phone has limited battery...'

# Initialize variables
clue = ''
location = ''
answer = ''
PLAYING = True
PLAYER1_NAME = ''
PLAYER2_NAME = ''

# CLUES ##################################################################

clues = queue.Queue()

# memory, location, answer found @ location
text = [('You wake up in a dingy classroom without power. It looks familiar but feels slightly different. There is no one around you. You cannot recall any of the events that happened the night before. There are things scattered around the room. You open your phone and can only access discord. You notice '+ PLAYER2_NAME + 'is online. Maybe they can help find out where you are? Try sending them a message.', 'wvh', 'INSERT_ONSITE CLUE_HERE'),
        ('Next, you went to a place with a lot of computers', 'khoury', 'INSERT_ONSITE CLUE_HERE'),
        ('What is the student center called?', 'curry', 'INSERT_ONSITE CLUE_HERE')]

for triplet in text:
    clues.put(triplet)

##########################################################################


# Gets the next clue in the from the queue. Updates clue and answer
def get_next_clue():
    global clue
    global location
    global answer

    pair = clues.get()
    clue = pair[0]
    location = pair[1]
    answer = pair[2]

# Increase battery by the given amount. Battery cannot exceed 100.
def inc_battery(increase):
  global battery
  if battery + increase > 100:
      battery = 100
  else:
      battery += increase


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
        print('Set player 1: ' + str(user.name))
        global PLAYER1_NAME
        PLAYER1_NAME = str(user.name)

    # Player 2: set playerID
    if reaction.emoji == EMOJI_2:
        PLAYER2_ID = user.id
        print('Set player 2: ' + str(user.name))
        global PLAYER2_NAME
        PLAYER2_NAME = str(user.name)


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
            await player1.send(
                "Message failed to send. Your phone seems buggy and won\'t send messages more than ' + str(MAX_HINT_LEN) + ' words long! Your message had "
                + str(len(hint)) + " words.")
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
        print("NO BATTERY LEFT 😭")
        #user = await client.fetch_user(int(PLAYER1_ID))
        #await user.send(NO_BATTERY_MSG)
        await channel.send(NO_BATTERY_MSG)
        PLAYING = False

    # Check channel for answer.
    if message.channel == channel:  #and message.author == player2
        # Check if won
        if message.content == answer:
            if clues.empty():
                PLAYING = False
                #channel = client.get_channel(int(CHANNEL_ID))
                await channel.send(WIN_MSG)

            # Send next clue
            else:
                await channel.send("That sounds familiar. " + PLAYER1_NAME + " is starting to remember what happened better now...")
                await channel.send("The electricity came back for a moment. " + PLAYER1_NAME + "\'s phone charged " + str(BATTERY_INC) + "%!")
                inc_battery(BATTERY_INC)
                await channel.send("Battery level: " + str(battery))
                print("SOLVED: " + answer)
                t = time()
                print("Time: " + str(ctime(t)))
                get_next_clue()
                #user = await client.fetch_user(int(PLAYER1_ID))
                #await user.send(clue)
                await player1.send(clue)
        elif message.content == location:
            await channel.send(PLAYER1_NAME + " remembers going there!")
            await channel.send("The electricity came back for a moment. " + PLAYER1_NAME + "\'s phone charged " + str(SMALL_BATTERY_INC) + "%!")
            inc_battery(SMALL_BATTERY_INC)
            await channel.send("Battery level: " + str(battery))
            print("SOLVED: " + clue)
            t = time()
            print("Time: " + str(ctime(t)))


# Run bot with token
client.run(os.getenv('TOKEN'))
