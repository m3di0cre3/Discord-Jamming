import discord
import os
import dotenv
dotenv.load_dotenv()

discord_token = str(os.getenv("DISCORD_TOKEN"))

bot = discord.Bot()
connections = {}

async def getting_audio(sink: discord.sinks, channel: discord.TextChannel, *args):
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio.get_data.items()
    ]
    await sink.vc.disconnect()
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)



@bot.command()
async def start_recording_vc(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("Currently not in a VC!")
    vc = await voice.channel.connect()
    connections.update({ctx.guild.id:vc})
    vc.start_recording(
        discord.sinks.WaveSink(),
        getting_audio,
        ctx.channel
    )
    await ctx.respond("Currently recording!")

@bot.command()
async def stop_recording_vc(ctx):
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("Currently not in a VC!")

bot.run(discord_token)