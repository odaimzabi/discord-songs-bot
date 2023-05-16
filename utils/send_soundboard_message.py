import discord

from discord.ui import Button, View
from utils.run_song import run_song
from utils.utils import get_songs


# TODO : delete the user comment after displaying the board


async def send_soundboard_message(channel, ffmpeg_path):
    print("Displaying soundboard...")
    songs = get_songs("./songs")
    view = View()

    for song in songs:
        button = Button(label=song, style=discord.ButtonStyle.primary, custom_id=song)
        button.callback = lambda interaction: run_song(interaction, ffmpeg_path)
        # Create a view and add the button to it
        view.add_item(button)

    # Send the message with the button
    # Process commands after reacting with like emoji
    await channel.send("this is a test", view=view)
