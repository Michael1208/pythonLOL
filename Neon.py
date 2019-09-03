import discord 
import os
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time

bot = commands.Bot(command_prefix='*')
TOKEN = os.environ['TOKEN']
bot.remove_command('help')

@bot.listen()
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----------')
    game = discord.Game("In Development")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
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

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Neon - Help & Documentation", color=0x6AA84F)
    embed.add_field(name='``*help``', value="Show this message", inline=False)
    embed.add_field(name="``*ping``",     value="Returns pong!", inline=False)
    embed.add_field(name="``*purge``", value="Purges (amount of messages!", inline=False)
    embed.add_field(name="``*ban``", value="Bans a user from the server! (BAN Permissions)", inline=False)
    embed.add_field(name="**Invite Neon**", value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
