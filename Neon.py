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

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx):
    start = time.monotonic()
    embed = discord.Embed(title="Neon's Ping!", color=0x0084FD)
    embed.add_field(name="latency", value="{} ms".format(int(ctx.bot.latency*1000)))
    await ctx.send(embed=embed)

bot.run(TOKEN)
