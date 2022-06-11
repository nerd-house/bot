import discord
from discord.ext import commands
import datetime
import sqlite3


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

# kick
    @commands.command()
    @commands.has_permissions(administrator =True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is not None:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(title="User Kicked!",colour=discord.Colour.green())
                embed.set_thumbnail(url=str(member.avatar_url))
                embed.add_field(name="**user Kicked**",value=f"**{member}**", inline=False)
                embed.add_field(name="**Kicked by**",value=f"**{ctx.author}**", inline=False)
                embed.add_field(name="**Reason:**",value=f"**{reason}**", inline=False)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                await member.send(embed=embed)
            except:
                await member.kick(reason=reason)


    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="User banned!",colour=discord.Colour.green())
            embed.set_thumbnail(str(url=member.avatar_url))
            embed.add_field(name="**User banned**",value=f"**{member}**", inline=False)
            embed.add_field(name="**Banned by**",value=f"**{ctx.author}**", inline=False)
            embed.add_field(name="**Reason:**",value=f"**{reason}**", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            await member.send(embed=embed)
        except:
            await member.ban(reason=reason)


    @kick.error
    async def on_kick_error(self,ctx,error,member: discord.Member = None):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("arrey lawda kisko kick kru??????")
      elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You can't use that {ctx.author.mention}")



    @commands.command(aliases=['purge'])
    @commands.has_permissions(kick_members=True)
    async def nuke(self,ctx,amount=500):
      await ctx.channel.purge(limit = amount)
      await ctx.send("nuked!")
      await ctx.send("https://imgur.com/LIyGeCR")



    @commands.command(name="lockchannel", aliases=['lock'])
    @commands.has_guild_permissions(manage_guild=True)
    async def lockchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        for role in ctx.guild.roles:
            if role.permissions.administrator:
                await channel.set_permissions(role, send_messages=True, read_messages=True)
            elif role.name == "@everyone":
                await channel.set_permissions(role, send_messages=False)

        await ctx.send(f"🔒The channel {channel.mention} has been locked")

    @commands.command(name="unlockchannel", aliases=['unlock'])
    @commands.has_guild_permissions(manage_guild=True)
    async def unlockchannel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(ctx.guild.roles[0], send_messages=True)

        await ctx.send(f"🔓The channel {channel.mention} has been unlocked")

    @commands.command(name="slowmode", aliases=['slm'])
    @commands.has_guild_permissions(manage_guild=True)
    async def setdelay(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode in this channel to **{seconds}** seconds!")


def setup(client):
    client.add_cog(Moderation(client))
    print("Logged Moderation Cod ")