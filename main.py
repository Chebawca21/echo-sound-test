import os
import asyncio
from dotenv import load_dotenv
import pydub
import discord
from discord.ext import commands
from discord.sinks import MP3Sink

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def finished_callback(sink: MP3Sink):
    mention_strs = []
    audio_segs: list[pydub.AudioSegment] = []
    files: list[discord.File] = []

    longest = pydub.AudioSegment.empty()

    for user_id, audio in sink.audio_data.items():
        mention_strs.append(f"<@{user_id}>")

        seg = pydub.AudioSegment.from_file(audio.file, format="mp3")

        if len(seg) > len(longest):
            audio_segs.append(longest)
            longest = seg
        else:
            audio_segs.append(seg)

        audio.file.seek(0)
        files.append(discord.File(audio.file, filename=f"{user_id}.mp3"))

    for seg in audio_segs:
        longest = longest.overlay(seg)

    longest.export("sounds/recording.mp3", format="mp3")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def echo(ctx):
    if ctx.author.voice is not None:
        user_channel = ctx.author.voice.channel
        voice_client = await user_channel.connect()
        audio1 = discord.FFmpegPCMAudio(source='sounds/echo1.wav')
        audio2 = discord.FFmpegPCMAudio(source='sounds/echo2.wav')
        ding = discord.FFmpegPCMAudio(source='sounds/ding.wav')

        if voice_client:
            await asyncio.sleep(2)
            await voice_client.play(audio1, wait_finish=True)

            voice_client.start_recording(MP3Sink(), finished_callback, sync_start=True)
            await asyncio.sleep(5)
            voice_client.stop_recording()
            await voice_client.play(ding, wait_finish=True)
            ding = discord.FFmpegPCMAudio(source='sounds/ding.wav')

            recording = discord.FFmpegPCMAudio(source='sounds/recording.mp3')
            await voice_client.play(recording, wait_finish=True)
            await voice_client.play(ding, wait_finish=True)
            await voice_client.play(audio2, wait_finish=True)

            await voice_client.disconnect()
    else:
        await ctx.send(f"User {ctx.author.mention} not in channel")


bot.run(os.getenv('BOT_TOKEN'))