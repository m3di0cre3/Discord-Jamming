import discord
from discord.ext import commands
import os
import numpy as np
import socket

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = '1248828890458361866'

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_address = ('localhost', 12345)  


class AudioCapture(discord.AudioSink):
    def __init__(self, socket):
        self.socket = socket
        super().__init__()

    def write(self, data):
        self.socket.sendto(data.data, udp_address)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        vc.start_recording(AudioCapture(udp_sock), ctx.channel)
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send('You are not connected to a voice channel.')

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Disconnected from the voice channel')
    else:
        await ctx.send('I am not in a voice channel.')

bot.run(TOKEN)