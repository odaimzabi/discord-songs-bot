from discord import FFmpegPCMAudio


async def run_song(interaction, ffmpeg_path, song="omg_wow"):
    print(f"Joining voice channel...")
    await interaction.response.send_message("Joining voice channel...")
    channel = interaction.user.voice.channel
    voice_client = await channel.connect()
    print(f"playing {song}...")
    voice_client.play(
        FFmpegPCMAudio(executable=ffmpeg_path, source="./songs/" + song + ".mp3")
    )
    while voice_client.is_playing():
        pass
    await voice_client.disconnect()
