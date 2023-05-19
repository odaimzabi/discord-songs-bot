from asyncio import sleep
import random
import discord
import os
import platform
import getpass
import fnmatch

from pathlib import Path

from discord.ext import commands
from dotenv import load_dotenv
from utils.run_song import run_song
from utils.send_soundboard_message import send_soundboard_message


# Variables declaration
dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)
emojis = ["😂", "😄", "😊", "😍", "👍", "😱", "🙌", "💩", "👏", "😜", "🎉", "😁", "💖"]
isDebugModeEnabled = False


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
    global isDebugModeEnabled

    # Don't respond to ourselves
    if message.author == bot.user:
        return

    # Print the message to the console
    print(f"Message from {message.author.name}: {message.content}")

    # React to every message with a like emoji
    random_emoji = random.choice(emojis)
    await message.add_reaction(random_emoji)
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

    if message.content.lower() == "toggle-debug-mode":
        isDebugModeEnabled = not isDebugModeEnabled

    if message.content.lower() == "display-sounds-board":
        await send_soundboard_message(message.channel, ffmpeg_path)

    if message.content.lower() == "where-are-you":
        if isDebugModeEnabled:
            await systemInfo(message.channel)

    await upload_audio_files(message)

    # Process commands after reacting with like emoji
    await bot.process_commands(message)

    counter = 0

    await sleep(10)
    async for _ in message.channel.history(limit=None):
        counter += 1

    if counter > 1:
        await clear(message.channel)
        await send_soundboard_message(message.channel, ffmpeg_path)


@bot.event
async def on_ready():
    global isDebugModeEnabled
    print(f"Welcome Djaraba gang. {bot.user} is Here. Use me well :D ")

    # Get the channel object using the channel ID
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(
            f"Welcome me in Jraba Safi Gang 😍. {bot.user} is Here 😜. Use me well 💖 "
        )

        # Clearing channel
        await clear(channel)

        # Send a message to the channel
        await send_soundboard_message(channel, ffmpeg_path)


@bot.event
async def on_interaction(interaction):
    if interaction.user.voice is None:
        print("User is not connected to any channel.")
        await interaction.response.send_message(
            "You are not connected to a voice channel!"
        )
        return

    await run_song(interaction, ffmpeg_path, interaction.data["custom_id"])


async def upload_audio_files(message):
    if message.channel.id == channel_id:
        for attachment in message.attachments:
            if attachment.filename.endswith((".mp3", ".wav", ".flac")):
                filepath = os.path.join("./songs", attachment.filename)
                # Check if file already exists
                if not os.path.isfile(filepath):
                    # Download the file
                    await attachment.save(filepath)
                    print("Downloaded file: " + attachment.filename)


@bot.command(name="delete-song")
async def delete_file(ctx, song):
    directory = "./songs/"
    try:
        for filename in os.listdir(directory):
            if fnmatch.fnmatch(filename, song + "*"):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)
                await ctx.send("File {} has been deleted.".format(song))
    except Exception as e:
        await ctx.send("An error occurred while deleting the file: {}".format(e))


@commands.has_permissions(manage_messages=True)
async def clear(channel):
    await channel.purge(limit=None)


async def systemInfo(channel):
    # Get OS information
    os_info = platform.system() + " " + platform.release()
    # Get the current username
    username = getpass.getuser()
    await channel.send(f"I am running in {os_info}. In the name of {username}")
    await send_soundboard_message(channel, ffmpeg_path)


bot.run(api_token)
