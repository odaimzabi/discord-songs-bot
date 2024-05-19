import asyncio
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

# Load environment variables
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

bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree


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

    await asyncio.sleep(10)
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

        # Sync commands with the guild and globally
        try:
            await tree.sync(guild=discord.Object(id=channel.guild.id))
            print("Slash commands have been synced with the guild.")
            await tree.sync()
            print("Slash commands have been synced globally.")
        except Exception as e:
            print(f"An error occurred while syncing commands: {e}")


@bot.event
async def on_interaction(interaction):
    if interaction.user.voice is None:
        print("User is not connected to any channel.")
        await interaction.response.send_message(
            "You are not connected to a voice channel!"
        )
        return

    await run_song(interaction, ffmpeg_path, interaction.data["custom_id"])


@tree.command(name="upload", description="Upload an audio file")
@app_commands.describe(name="Name of the song", emoji="Emoji for the song", attachment="Song audio file (.mp3, .wav, .flac)")
async def upload_audio_files(interaction: discord.Interaction, name: str, emoji: str):
    print("Upload command received!")
    if interaction.channel_id == channel_id:
        data = await getSongConfigs()
        # Check if a song with the same name already exists
        if any(item["name"] == name for item in data):
            await interaction.response.send_message(f"A song with the name '{name}' already exists.")
            return

        for attachment in interaction.attachments:
            if attachment.filename.endswith((".mp3", ".wav", ".flac")):
                filepath = os.path.join("./songs", attachment.filename)
                # Check if file already exists in the directory
                if not os.path.isfile(filepath):
                    # Download the file
                    await attachment.save(filepath)
                    print("Downloaded file: " + attachment.filename)
                    # Add the song to the JSON config
                    await add_to_json(emoji, name, attachment.filename)
                    await interaction.response.send_message(f"File '{name}' has been uploaded and saved.")
                else:
                    await interaction.response.send_message(f"File '{attachment.filename}' already exists in the directory.")
    else:
        await interaction.response.send_message("This command can only be used in the designated channel.")


@tree.command(name="delete_song", description="Delete an audio file")
@app_commands.describe(song="Name of the song to delete")
async def delete_file(interaction: discord.Interaction, song: str):
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
                await interaction.response.send_message(f"File {filename} has been deleted.")
                break

        if not file_deleted:
            await interaction.response.send_message(f"File {uri} not found in the directory.")

        # Remove the song config from the data
        new_data = [item for item in data if item.get("name") != song]
        if len(new_data) == len(data):
            await interaction.response.send_message(f"Song {song} not found in the config file.")
        else:
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(new_data, file, ensure_ascii=False, indent=2)
            await interaction.response.send_message(f"Song {song} has been removed from the config file.")

    except Exception as e:
        await interaction.response.send_message(f"An error occurred while deleting the file: {e}")


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


@tree.command(name="die", description="Shut down the bot")
async def die(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bye :pleading_face:")
    exit(0)


bot.run(api_token)
