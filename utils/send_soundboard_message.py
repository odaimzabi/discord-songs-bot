import discord
from discord.ext import commands

from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ui import Button, View
from utils.run_song import run_song

async def send_soundboard_message(bot, channel):
      
    button = Button(label='Click Me!', style=discord.ButtonStyle.primary, custom_id="my_button")
    button.callback=lambda interaction: run_song(interaction,message,ffmpeg_path)
    # Create a view and add the button to it
    view = View()
    view.add_item(button)

    # Send the message with the button
    # Process commands after reacting with like emoji
    await channel.send("this is a test",view=view)