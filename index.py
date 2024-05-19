from asyncio import sleep
import random
import discord
import os
import platform
import getpass
import fnmatch
import json

from pathlib import Path

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils.run_song import run_song
from utils.send_soundboard_message import send_soundboard_message
from utils.utils import getSongConfigs, saveSongConfigs, help_message

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

    if message.content.lower() == "toggle-debug-mode":
        isDebugModeEnabled = not isDebugModeEnabled

    if message.content.lower() == "display-sounds-board":
        await send_soundboard_message(message.channel, ffmpeg_path)

    if message.content.lower() == "where-are-you":
        if isDebugModeEnabled:
            await systemInfo(message.channel)

    # Process commands after reacting with like emoji
    await bot.process_commands(message)

    counter = 0

    await sleep(10)
    async for _ in message.channel.history(limit=None):
        counter += 1

    if counter > 10:
        await clear(message.channel)
        await send_soundboard_message(message.channel, ffmpeg_path)


@bot.event
async def on_ready():
    global isDebugModeEnabled
    print(f"Welcome Djaraba gang. {bot.user} is Here. Use me well :D ")

    # Get the channel object using the channel ID
    channel = bot.get_channel(channel_id)
    # Clearing channel
    await clear(channel)
    if channel:
        await channel.send(
            f"Welcome me in Jraba Safi Gang 😍. {bot.user} is Here 😜. Use me well 💖 "
        )

        await help_message(channel)

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


@bot.command(name="upload")
async def upload_audio_files(ctx, name, emoji):
    print("Upload command received!")
    if ctx.channel.id == channel_id:
        data = await getSongConfigs()
        # Check if a song with the same name already exists
        if any(item["name"] == name for item in data):
            await ctx.send(f"A song with the name '{name}' already exists.")
            return

        for attachment in ctx.message.attachments:
            if attachment.filename.endswith((".mp3", ".wav", ".flac")):
                filepath = os.path.join("./songs", attachment.filename)
                # Check if file already exists in the directory
                if not os.path.isfile(filepath):
                    # Download the file
                    await attachment.save(filepath)
                    print("Downloaded file: " + attachment.filename)
                    # Add the song to the JSON config
                    await add_to_json(emoji, name, attachment.filename)
                    await ctx.send(f"File '{name}' has been uploaded and saved.")
                else:
                    await ctx.send(f"File '{attachment.filename}' already exists in the directory.")
    else:
        await ctx.send("This command can only be used in the designated channel.")

@bot.command(name="delete-song")
async def delete_file(ctx, song):
    directory = "./songs/"
    data = await getSongConfigs()
    uri = next((item.get("uri") for item in data if item.get("name") == song), song + ".mp3")
    try:
        file_deleted = False
        for filename in os.listdir(directory):
            if fnmatch.fnmatch(filename, uri):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)
                file_deleted = True
                await ctx.send(f"File {filename} has been deleted.")
                break

        if not file_deleted:
            await ctx.send(f"File {uri} not found in the directory.")

        # Remove the song config from the data
        new_data = [item for item in data if item.get("name") != song]
        if len(new_data) == len(data):
            await ctx.send(f"Song {song} not found in the config file.")
        else:
            await saveSongConfigs(new_data)
            await ctx.send(f"Song {song} has been removed from the config file.")

    except Exception as e:
        await ctx.send(f"An error occurred while deleting the file: {e}")

async def add_to_json(emoji, name, filename):
    # Load the existing JSON file into a dictionary
    data = await getSongConfigs()

    # Add the emoji and name to the dictionary
    data.append({
        "emoji": emoji,
        "name": name,
        "uri": filename
    })

    # Save the updated dictionary back to the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file)


@commands.has_permissions(manage_messages=True)
async def clear(channel):
    if channel.id == channel_id:
        await channel.purge(limit=None)


async def systemInfo(channel):
    # Get OS information
    os_info = platform.system() + " " + platform.release()
    # Get the current username
    username = getpass.getuser()
    await channel.send(f"I am running in {os_info}. In the name of {username}")
    await send_soundboard_message(channel, ffmpeg_path)

@bot.command(name="die")
async def die(ctx):
    await ctx.send(f"Bye :pleading_face: ")
    exit(0)

bot.run(api_token)
