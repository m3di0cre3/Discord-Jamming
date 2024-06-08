import discord
import os
import dotenv
dotenv.load_dotenv()

discord_token = str(os.getenv("DISCORD_TOKEN"))

bot = discord.Bot()
connections = {}

@bot.event
async def on_ready():
    print("Bot Is Working and Online!")
    print('--------------------------')

@bot.command
async def hello(ctx,*,user_input:str):
    await ctx.send(user_input)

bot.run(discord_token)