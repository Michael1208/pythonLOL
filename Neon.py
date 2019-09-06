import discord 
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time
import random
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
    embed.add_field(name="**n.botinfo**", value="Get information on the bot and the developers!", inline=False)
    embed.add_field(name="**n.userinfo**", value="Displays info on the mentioned user", inline=False)
    embed.add_field(name="**n.invite**", value="Displays bot and support server invite", inline=False)
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
async def echo(ctx, *, text=None):
    if text == '@everyone, @here':
        await ctx.send("Please don't ping everyone")
    else:
        await ctx.send(f"{text}")
 
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
    role = discord.utils.get(ctx.guild.roles, name="Muted")
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
    role = discord.utils.get(ctx.guild.roles, name="Muted")
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

@bot.command()
async def botinfo(ctx):
    embed=discord.Embed(title='[Support Server](https://discord.gg/WqtTxNV)', description="**About Neon Bot**", color=0xff3899)
    embed.set_author(name="Neon Bot")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/616619124730363924/6ad4db462a2e98a94b69dc5a8bd7534f.png?")
    embed.add_field(name='What Is Neon', value="Neon Is A Bot Coded In Discord.py Rewrite It Has Multiple Features Such As Moderation, Fun And, Music (Music In Development)" , inline=False)
    embed.add_field(name='The Bot Owners', value="Bot Developers", inline=True)
    embed.add_field(name='Kyle♡#1849', value="Kyle Is Just An Average Guy Born On December 9th 2004 Who Likes To Code And Use Discord", inline=False)
    embed.add_field(name='Michael♡#3910', value="Michael Is Again Just An Average Guy Who Likes Coding Born June 8th 2005", inline=False)
    embed.set_footer(text='Neon Bot')
    await ctx.send(embed=embed)
										
@bot.command(pass_context=True)
async def balance(ctx):
    ''': Check your balance!'''
    member=ctx.message.author
    check_id(member.id)
    await bot.reply(f'you have {currency.data[member.id]} {currency.data["name"]}')

@bot.command()
async def userinfo(ctx, member: discord.Member):
	
	roles = [role for role in member.roles]
	
	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
	
	embed.set_author(name=f"User Info - {member}")
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
	
	embed.add_field(name="ID:", value=member.id)
	embed.add_field(name="Guild name:", value=member.display_name)
	
	embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	
	embed.add_field(name=f"Roles ((len(roles)))", value=" ".join([role.mention for role in roles]))
	embed.add_field(name="Top role:", value=member.top_role.mention)
	
	embed.add_field(name="Bot?", value=member.bot)
	
	await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def register(ctx):
    id = ctx.message.author.id
    channel = ctx.message.channel
    if id not in Credits:
        Credits[id] = 100
        await channel.send(f"You are now registered and have been given 100 Credits {ctx.message.author.mention}")
        _save()
    else:
        await channel.send(f"You already have an account {ctx.message.author.mention}")

@bot.command()
async def level(self, ctx, user: discord.Member = None):
        user = ctx.author if not user else user
        user_id = str(user.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", user_id, guild_id)

        if not user:
            await ctx.send("Member doesen't have a level")
        else:
            embed = discord.Embed(color=ctx.message.author.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level - {user}", icon_url=self.bot.user.avatar_url)

            embed.add_field(name="Level", value=int(user[0]['lvl']))
            embed.add_field(name="XP", value=int(user[0]['xp']))

            await ctx.send(embed=embed)

bot.run(TOKEN)
