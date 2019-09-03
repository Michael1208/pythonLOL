import discord 
import os
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time

bot = commands.Bot(command_prefix='*')
TOKEN = os.environ['TOKEN']

@bot.listen()
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    game = discord.Game("In Development")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx):
    start = time.monotonic()
    embed = discord.Embed(title="Neon's Ping!", color=0x0084FD)
    embed.add_field(name="latency", value="{} ms".format(int(ctx.bot.latency*1000)))
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please mention a user to ban")
    else:
        await member.ban(reason=reason)

@bot.command()
async def purge(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

bot.run(TOKEN)
