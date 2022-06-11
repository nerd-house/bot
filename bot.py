import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
import asyncio
import os


intents = discord.Intents.all()
client = commands.Bot(command_prefix=when_mentioned_or("."),intents=intents)


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print('Servers connected to:')
	for guild in client.guilds:
		print(f"{guild.name}\n{len(guild.members)}")


async def status():
  while True:
    await client.wait_until_ready()

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(client.guilds)} Servers! |.help '))
    await asyncio.sleep(5)
    await client.loop.create_task(status())

async def on_message( message):
    print('Message from {0.author}: {0.content}'.format(message))


@client.command()
async def ping(ctx):
	# await ctx.send(f'Pong {round(client.latency*1000)}ms')
	embed = discord.Embed(Title="🏓 Ping",
	                      color=discord.Colour.green())
	embed.add_field(
	    name="API Ping",
	    value=f"🏓 {round(client.latency*1000)}ms")
	await ctx.send(embed=embed)

@client.command(pass_context=True)
async def serverinfo(ctx,member: discord.Member = None):
    """Displays server information."""
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0x176cd5)
    embed.add_field(name="Server Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.guild.members))
    embed.add_field(name="Channels", value=len(ctx.message.guild.channels))
    embed.add_field(name="Region", value=ctx.message.guild.region)
    embed.add_field(name="Verification Level", value=ctx.message.guild.verification_level)
    # embed.add_field(name="Owner", value=ctx.message.guild.owner.mention)
    embed.add_field(name="Emojis", value=len(ctx.message.guild.emojis))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
    # embed.set_footer(text="Server ID is " + ctx.message.guild.id)
    await ctx.send(embed=embed)



@client.command()
async def hello(ctx):
    await ctx.reply(f"Hello {ctx.author.name}")

@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'Loaded {extension}')


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')


@load.error
async def load_error(ctx, error):
	await ctx.send('Invalid use of command')




token = "OTg1MDYzMTMxOTI1NjEwNDk3.GrMYTy.hnIhyJrumf_DgZb1I0bUVcSSQgOr605SlUkxak"
client.run(token)
