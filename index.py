import discord
from discord.ext import commands

from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ui import Button, View

from utils.run_song import run_song
from utils.send_soundboard_message import send_soundboard_message
import os 

from pathlib import Path

# Env variables
dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

ffmpeg_path, channel_id=os.getenv("FFMPEG"), int(os.getenv("CHANNEL_ID"))

# Intents
intents = discord.Intents.default()
intents.message_content=True
intents.messages=True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return

    # Print the message to the console
    print(f'Message from {message.author.name}: {message.content}')

    # React to every message with a like emoji
    await message.add_reaction('👍')
    if message.content.lower() == "clap":
      
        ctx = await bot.get_context(message)

        button = Button(label='Click Me!', style=discord.ButtonStyle.primary)
        button.callback=lambda interaction: run_song(interaction, message, ffmpeg_path)
        # Create a view and add the button to it
        view = View()
        view.add_item(button)

        # Send the message with the button
        await ctx.send('This is a message with a button!', view=view)
        # Process commands after reacting with like emoji
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Get the channel object using the channel ID
    channel = bot.get_channel(channel_id)
    if channel:
        # Send a message to the channel
       await send_soundboard_message(bot, channel)

@bot.event
async def on_interaction(interaction):
    # print(interaction.message)
    # print(interaction.application_id)
    # print(interaction.namespace)
    # print(interaction.data)
   await run_song(interaction,ffmpeg_path)


    


bot.run(os.getenv('API_TOKEN'))