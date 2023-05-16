import discord
from discord.ext import commands

from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ui import Button, View

async def run_song(interaction: discord.Interaction, ffmpeg_path):
    print(interaction)
    await interaction.response.send_message('Joining voice channel...')
    if interaction.user.voice is None:
            await message.channel.send("You are not connected to a voice channel!")
            return
    voice_channel = interaction.user.voice.channel
    voice_client = await voice_channel.connect()
    voice_client.play(FFmpegPCMAudio(executable=ffmpeg_path, source="./songs/omg_wow.mp3"))
    while voice_client.is_playing():
            pass
    await voice_client.disconnect()