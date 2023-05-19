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
        # This is not needed so far.
        #button.callback = lambda interaction: run_song(interaction, ffmpeg_path, song)
        # Create a view and add the button to it
        view.add_item(button)

    # Send the message with the button
    # Process commands after reacting with like emoji
    await channel.send("Here you go, displaying play board. \nHave fun", view=view)
