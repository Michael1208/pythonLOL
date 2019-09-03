import discord 
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time
import random
import json
import os
from discord.ext import commands, tasks
from itertools import cycle

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
    embed.add_field(name='***help**', value="Show this message", inline=False)
    embed.add_field(name="***ping**",     value="Returns pong!", inline=False)
    embed.add_field(name="***purge**", value="Purges (amount of messages! (Requires Manage Messages)", inline=False)
    embed.add_field(name="***ban**", value="Bans a user from the server! (Requires BAN Permissions)", inline=False)
    embed.add_field(name="**Invite Neon**", value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False)
    embed.add_field(name="***echo**", value="Repeats your message!", inline=False)
    await ctx.send(embed=embed)

status = cycle(['*help','In Development'])

@bot.event

async def on_ready():

	change_status.start()

	print("Neon has started!")				
		
@tasks.loop(seconds=15)

async def change_status():

	await bot.change_presence(activity=discord.Game(next(status)))

@bot.command()
async def echo(ctx,*,args):
	output = ''
	for word in args:
		output += word
		output += ''
	await ctx.send(output)
 
@bot.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	
@bot.command(pass_context=True)
async def leave(ctx):
	guild = ctx.message.guild
	voice_bot = guild.voice_bot_in(server)
	await voice_bot.disconnect()
	
@bot.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_bot = bot.voice_bot_in(server)
	player = await voice_bot.create_ytdl_player(url)
	players[server.id] = player
	player.start()

bot.run(TOKEN)
