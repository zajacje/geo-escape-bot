import discord
import os

from clues import clues

# Connect to discord
client = discord.Client()

# Get channel
DM_ID = 890313505981493258
CHANNEL_ID = 890334525979242578

# Initialize variables
clue = ''
answer = ''
PLAYING = True
battery = 100

# Gets the next clue in the from the queue. Updates clue and answer
def get_next_clue():
  global clue 
  global answer

  pair = clues.get()
  clue = pair[0]
  answer = pair[1]

@client.event
async def on_ready(): # callback
  print('We have logged in as {0.user}'.format(client))
  get_next_clue()
  channel = client.get_channel(int(DM_ID))
  await channel.send("Battery level: " + str(battery))
  await channel.send(clue)

# Receives message and responds
@client.event
async def on_message(message):
  # If message if sent from ourselves, do nothing
  if message.author == client.user:
      return

  global PLAYING
  if PLAYING:
    global battery
    battery -= 2
    channel = client.get_channel(int(DM_ID))
    await channel.send("Battery level: " + str(battery))

  if battery == 0:
    channel = client.get_channel(int(DM_ID))
    await channel.send("Your phone ran out of battery :(")
    PLAYING = False

  if message.content == answer:
    if clues.empty():
      PLAYING = False
      channel = client.get_channel(int(DM_ID))
      await channel.send('Congratulations!')

    else:
      get_next_clue()
      channel = client.get_channel(int(DM_ID))
      await channel.send(clue)


# Run bot with token
client.run(os.getenv('TOKEN'))

