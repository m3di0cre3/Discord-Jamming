import discord
import os
import numpy as np
import socket

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = '1248828890458361866'

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

class AudioCapture(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.voice_client = None
        client = discord.Client(intents = intents)


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        channel = self.get_channel(int(CHANNEL_ID))
        self.voice_client = await channel.connect()

    """
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.id == int(CHANNEL_ID):
            if self.voice_client is None or not self.voice_client.is_connected():
                channel = self.get_channel(int(CHANNEL_ID))
                self.voice_client = await channel.connect()
            else:
                self.voice_client.listen(discord.sinks.PCMAudioSink(self.process_audio))
    """
    @client.event
    def process_audio(self, data):
        # Convert data to numpy array
        print("test")
        audio_array = np.frombuffer(data, dtype=np.int16)
        # Send the audio data over the socket
        print(audio_array)
        self.sock.sendto(audio_array.tobytes(), ("localhost", 65436))

    async def on_disconnect(self):
        await self.voice_client.disconnect()
        self.sock.close()

client = AudioCapture()
client.run(TOKEN)
