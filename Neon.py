import discord 
import os
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='*')
TOKEN = os.environ['TOKEN']

@bot.event
async def on_ready():
    print('Bot is ready!')
    print(bot.user.name)
    print(bot.user.id)

bot.run(TOKEN)
