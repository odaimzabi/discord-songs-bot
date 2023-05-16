from discord import FFmpegPCMAudio


async def run_song(channel, ffmpeg_path, song="./songs/omg_wow.mp3"):
    voice_client = await channel.connect()
    voice_client.play(FFmpegPCMAudio(executable=ffmpeg_path, source=song))
    while voice_client.is_playing():
        pass
    await voice_client.disconnect()
