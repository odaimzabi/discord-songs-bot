from discord import FFmpegPCMAudio


async def run_song(channel, ffmpeg_path, song="omg_wow"):
    voice_client = await channel.connect()
    voice_client.play(
        FFmpegPCMAudio(executable=ffmpeg_path, source="./songs/" + song + ".mp3")
    )
    while voice_client.is_playing():
        pass
    await voice_client.disconnect()
