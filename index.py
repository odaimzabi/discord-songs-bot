import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

from pathlib import Path

from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents.default()
intents.message_content=True

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
        if message.author.voice is None:
            await message.channel.send("You are not connected to a voice channel!")
            return
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        voice_client.play(FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="/songs/omg_wow.mp3"))
        while voice_client.is_playing():
            pass
        await voice_client.disconnect()
    
    # Process commands after reacting with like emoji
    await bot.process_commands(message)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')


bot.run(os.getenv('API_TOKEN'))