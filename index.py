import discord
from discord.ext import commands

from dotenv import load_dotenv

from utils.run_song import run_song
from utils.send_soundboard_message import send_soundboard_message
import os

from pathlib import Path

# Env variables
dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)

ffmpeg_path, channel_id, api_token = (
    os.getenv("FFMPEG"),
    int(os.getenv("CHANNEL_ID")),
    os.getenv("API_TOKEN"),
)

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return

    # Print the message to the console
    print(f"Message from {message.author.name}: {message.content}")

    # React to every message with a like emoji
    await message.add_reaction("👍")
    # if message.content.lower() == "clap":
    #     ctx = await bot.get_context(message)

    #     button = Button(label="Click Me!", style=discord.ButtonStyle.primary)
    #     button.callback = lambda interaction: run_song(
    #         interaction, message, ffmpeg_path
    #     )
    #     # Create a view and add the button to it
    #     view = View()
    #     view.add_item(button)

    #     # Send the message with the button
    #     await ctx.send("This is a message with a button!", view=view)
    #     # Process commands after reacting with like emoji
    #     await bot.process_commands(message)
    if message.content.lower() == "!dsb":
        await send_soundboard_message(message.channel, ffmpeg_path)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Get the channel object using the channel ID
    channel = bot.get_channel(channel_id)
    if channel:
        # Send a message to the channel
        await send_soundboard_message(channel, ffmpeg_path)


@bot.event
async def on_interaction(interaction):
    await interaction.response.send_message("Joining voice channel...")
    # if interaction.user.voice is None:
    #         await interaction.response.send_message("You are not connected to a voice channel!")
    #     return
    voice_channel = interaction.user.voice.channel
    await run_song(voice_channel, ffmpeg_path)


bot.run(api_token)
