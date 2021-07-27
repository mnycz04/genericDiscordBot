"""
Commands that can be used by everybody. Mostly for fun, but there is some use
"""
import logging
import os

import discord
from discord.ext import commands

from utilities import check_blacklist, check_valid_channel, get_mp3


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
        logger = logging.getLogger(str(ctx.guild.id))

        if await check_blacklist(ctx.guild, ctx.author):
            await ctx.send(f"Sorry <@!{ctx.author.id}>, you're blacklisted from using this command!",
                           delete_after=10)
            logger.info(f"{ctx.author.name} was barred from using the MP3 command.")
            return

        if not await check_valid_channel(ctx.guild, "music_cmds_channel", ctx.message):
            await ctx.send("You can't use this command in this channel!")
            logger.info(f"{ctx.author.name} was barred from using the MP3 command because of incorrect channel")
            return

        logger.info(f"Mp3 Requested by user \"{ctx.author.name},\" id: {ctx.author.id}")

        query = ''.join(query)
        logger.info(f"Query is: \"{query}\"")
        loading_embed = discord.Embed(title="Downloading Song...",
                                      color=int(hex(int("009dff", 16)), 0))
        loading_embed = await ctx.send(embed=loading_embed)
        try:
            song = await get_mp3(query)
            await ctx.send(embed=song[0], file=discord.File(song[1]))
        except Exception:
            await ctx.send("Error retrieving youtube video. It might not be a valid file.", delete_after=10)
        else:
            os.remove(f"{song[1]}")
        finally:
            await loading_embed.delete()
