from discord.ext import commands
import discord
from models.plex import Plex
from plexapi.audio import Album


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.plex = Plex()

    @commands.command(name='join')
    async def join_channel(self, ctx, *, channel_name):
        songsChannel = discord.utils.get(
            ctx.guild.voice_channels, name=channel_name)
        voiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if voiceClient:
            if voiceClient.is_connected():
                await ctx.send(f'Voice is already connected to {voiceClient.channel} channel!')
                return
        await songsChannel.connect()
        await ctx.send('Joined Voice Channel!')

    @join_channel.error
    async def join_channel_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('Channel name missing in command!')
            return
        raise error

    # @commands.command(name='play')
    async def play(self, ctx):
        voiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voiceClient:
            await ctx.send('Voice is not connected to a channel!')
            return
        URL = ''
        if not voiceClient.is_connected():
            await ctx.send('Not connected to a voice channel!')
            return
        voiceClient.play(discord.FFmpegPCMAudio(URL))

    @commands.command(name='pause')
    async def pause(self, ctx):
        voiceclient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voiceclient:
            await ctx.send('Voice is not connected to a channel!')
            return
        if not voiceclient.is_playing():
            await ctx.send('Nothing is being played!')
            return
        voiceclient.pause()

    @commands.command(name='resume')
    async def resume(self, ctx):
        voiceclient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voiceclient:
            await ctx.send('Voice is not connected to a channel!')
            return
        if not voiceclient.is_paused():
            await ctx.send('The voice is not paused!')
            return
        voiceclient.resume()

    @commands.command(name='stop')
    async def stop(self, ctx):
        voiceclient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voiceclient:
            await ctx.send('Voice is not connected!')
            return
        if not voiceclient.is_paused and not voiceclient.is_playing():
            await ctx.send('Nothing is being played!')
            return
        voiceclient.stop()
        await ctx.send('Voice Stopped!')

    @commands.command(name='disconnect')
    async def disconnect(self, ctx):
        voiceclient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voiceclient:
            await ctx.send('Voice is not connected!')
            return
        await voiceclient.disconnect()
        await ctx.send('Voice disconnected!!')

    @commands.command(name='search')
    async def search(self, ctx, *, query):
        res = await self.plex.searchServer(query)
        embed = discord.Embed(title='Search Results')
        for r in res:
            embed.add_field(name='id', value=res.index(r))
            embed.add_field(name='Title', value=r.title)
            sep = '-----------------------------'
            embed.add_field(name=sep, value=sep, inline=False)

        await ctx.send(embed=embed)

        def check(authorID):
            def inner(message):
                if not message.author.id == ctx.author.id:
                    return False
                if not message.channel == ctx.channel:
                    return False
                return True
            return inner

        await ctx.send('Enter the id of the track to play!\nEnter ; to cancel playing!')
        msg = await self.bot.wait_for('message', check=check(ctx.author.id))
        if msg.content == ';':
            return
        index = int(msg.content)
        URL = res[index].getStreamURL()
        title = res[index].title
        voiceClient = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if voiceClient is None:
            await ctx.send('Voice is not connected to a voice channel!')
            return
        await ctx.send(f'Now playing : {title}')
        voiceClient.play(discord.FFmpegPCMAudio(URL))


def setup(bot):
    bot.add_cog(Music(bot))
    print('Music extension loaded!')
