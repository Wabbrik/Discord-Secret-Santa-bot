import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
messageID = None
messageCH = None
client = discord.Client()
santaPhrases = [
    'HoHoHo!',
    'Seeing isn\'t believing',
    'Your mistletoe is no match for my TOW Missile!',
    'Ho... ho... ho. Oh, my heart\'s not in it. I\'m too depressed for murder and mayhem.',
    'I define GOOD!'
]

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    global messageID
    global messageCH
    if message.author == client.user:
        return

    if message.content == '!santa':
        global santaPhrases
        response = random.choice(santaPhrases)
        await message.channel.send(response)
        return

    if message.content == '!satan':
        await message.add_reaction('💢')
        return

    if message.content == '!santa event':
        if messageID != None:
            await message.channel.send("You've already started an event.")
            return
        response = "In order to participate to this event please react with a ✅ to this comment!"
        message = await message.channel.send(response)
        messageID = message.id
        messageCH = message.channel
        return

    if message.content == '!santa event end':
        if messageID == None:
            await message.channel.send('Please start an event first!')
            return
        else:
            originalMessage = await messageCH.fetch_message(messageID)
            users = None
            for reaction in originalMessage.reactions:
                if reaction.emoji == '✅':
                    users = await reaction.users().flatten()
                    break
            
            if users == None or len(users) < 2:
                messageID = None
                messageCH = None
                await message.channel.send("In order for the event to take place, more people need to take part in this event. Santa will write this on his list.")
                return 

            random.shuffle(users)
            for i in range(len(users)):
                temp = f"You will be {users[(i+1)%len(users)].name}\'s Secret Santa 🎅."
                await users[i].send(temp)
            await message.channel.send('Event ended, check your DMs.')
            
client.run(TOKEN)