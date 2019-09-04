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

bot = commands.Bot(command_prefix='n.')
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
    embed.add_field(name='**n.help**', value="Show this message", inline=False)
    embed.add_field(name="**n.ping**",     value="Returns pong!", inline=False)
    embed.add_field(name="**n.purge**", value="Purges (amount) of messages! (Requires Manage Messages)", inline=False)
    embed.add_field(name="**n.ban**", value="Bans a user from the server! (Requires Ban Permissions)", inline=False)
    embed.add_field(name="**n.echo**", value="Repeats your message!", inline=False)
    embed.add_field(name="**n.kick**", value="Kicks a user off the server! (Requires Kick Permissions)", inline=False)
    embed.add_field(name="**n.unban**", value="Unbans a user that was banned from the server! (Requires Ban Permissions)", inline=False)
    embed.add_field(name="**n.mute**", value="Mutes a user on the server! (Requires Mute Permissions)", inline=False)
    embed.add_field(name="**n.unmute**", value="Unmutes a user on the server! (Requires Mute Permissions)", inline=False)
    embed.add_field(name="**Invite Neon**", value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False)
    await ctx.send(embed=embed)

status = cycle(['n.help','In Development'])

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
	await bot.join_voice_channel(channel)
	
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

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please mention a user to kick")
    else:
        await member.kick(reason=reason)

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(role)
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to mute people")
 
 
@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(role)
@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You are not allowed to unmute people")

@bot.command()
async def invite(ctx):
	embed = discord.Embed(title="Neon - Invites", color=0x6AA84F)
	embed.add_field(name='**Invite Neon**', value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False)
	embed.add_field(name='**Support Server**', value="[Support](https://discord.gg/WqtTxNV)", inline=False)
	await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def balance(ctx):
    ''': Check your balance!'''
    member=ctx.message.author
    check_id(member.id)
    await bot.reply(f'you have {currency.data[member.id]} {currency.data["name"]}')

@bot.command(aliases=['leaderboards'])
async def leaderboard():
    ''': View the server leaderboad'''
    members=[(ID,score) for ID,score in currency.data.items() if ID !='name']
    if len(members)==0:
        await bot.say('I have nothing to show')
        return
    ordered=sorted(members,key=lambda x:x[1] ,reverse=True )
    players=''
    scores=''
    for ID,score in ordered:
        player=discord.utils.get(bot.get_all_members(),id=ID)
        players+=player.mention+'\n'
        scores+=str(score)+'\n'
    embed=discord.Embed(title='Leaderboard')
    embed.add_field(name="Player", value=f"{player}")
    embed.add_field(name="Player", value=f"{scores}") 
    await bot.say(embed=embed)

bot.run(TOKEN)
