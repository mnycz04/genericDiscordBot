"""
Commands that can be used by everybody. Mostly for fun, but there is some use
"""

import discord
from discord.ext import commands
from songHandler import Song


class MemberCommands(commands.Cog, name="Member Commands"):
    """
    Commands that may be used by almost anybody.
    """

    @commands.command(aliases=["mp3", "downloadsong", "dlsong", "dls"])
    async def download_mp3(self, ctx, *, query=None):
        """
        Searches Youtube for a video, and tries to send a downloaded mp3 in return
        Takes either a link, or just a search query
        """
        await ctx.message.delete()

        query = ''.join(query)
        song = Song()
        loading_embed = discord.Embed(title="Downloading Song...",
                                      color=int(hex(int("009dff", 16)), 0))
        loading_embed = await ctx.send(embed=loading_embed)
        try:
            song.song_query = query
            await song.download_song()
            duration_formatted = f"{int(song.song_duration // 60)}:{int(song.song_duration % 60)}"
            song_embed = discord.Embed(title=song.song_url,
                                       color=int(hex(int("009dff", 16)), 0))
            song_embed.set_image(url=song.song_thumbnail)
            song_embed.set_footer(text=f"Duration: {duration_formatted}")
            song_embed.set_author(name=song.song_name)
            await loading_embed.delete()
            await ctx.send(embed=song_embed, file=discord.File(f"{song.song_file_location}.{song.song_file_ext}",
                                                               f"{song.song_name}.{song.song_file_ext}".replace('-',
                                                                                                                '')
                                                               .strip()
                                                               .replace(' ', '-')))
        except Exception:
            await ctx.send("There was an error getting your file. It might not be compatible.", delete_after=5)
            await loading_embed.delete()
