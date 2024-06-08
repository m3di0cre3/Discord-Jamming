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


# Set up the UDP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_address = ('localhost', 12345)  # Replace with your server's IP and port

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        await ctx.send(f'Joined {channel}')
        await capture_audio(vc)
    else:
        await ctx.send('You are not connected to a voice channel.')

async def capture_audio(voice_client):
    while voice_client.is_connected():
        data = voice_client.recv_packet()
        udp_sock.sendto(data[1], udp_address)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Disconnected from the voice channel')
    else:
        await ctx.send('I am not in a voice channel.')

bot.run(TOKEN)
