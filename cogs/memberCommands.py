"""
Commands that can be used by everybody. Mostly for fun, but there is some use
"""
import logging
import os
from random import random

import discord
from discord.ext import commands

from utils.utilities import check_blacklist, check_valid_channel, get_mp3, get_reddit_post


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
        loading_embed.set_footer(text="Some large videos may take a while.")
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

    @commands.command(aliases=["r", "red", "sub"])
    async def reddit(self, ctx, *, subreddit):
        """Gets and sends a random post from a specified subreddit"""
        await ctx.message.delete()
        logger = logging.getLogger(str(ctx.guild.id))

        if await check_blacklist(ctx.guild, ctx.author):
            await ctx.send("You're blacklisted from this command!", delete_after=10)
            return

        if not await check_valid_channel(ctx.guild, "embed_channel", ctx):
            await ctx.send("Can use this command in this channel!", delete_after=10)
            return
        logger.info(f"Reddit command used by '{ctx.author.name}' for subreddit '{subreddit}'")

        try:
            post = await get_reddit_post(subreddit)
        except ConnectionRefusedError:
            await ctx.send(f"**{subreddit} doesn't like bots like me to retrieve posts.**", delete_after=10)
            logger.info("Subreddit doesn't allow bots.")
        except LookupError:
            await ctx.send(f"**{subreddit} was an invalid name.**", delete_after=10)
            logger.info("Subreddit name was invalid.")
        except Exception as error:
            await ctx.send("Unknown error occurred. Sorry!", delete_after=10)
            logger.exception("Unknown error occurred in getting a reddit post")
            logger.exception(error)
        else:
            video = False
            embed = discord.Embed(title=post.title, url=post.shortlink, color=int(hex(int("ff0000", 16)), 0))
            if '.jpg' in post.url:
                embed.set_image(url=post.url)
            elif ('v.redd.it' in post.url) or ('youtu' in post.url):
                video = True
            embed.set_author(name=post.author.name)
            embed.set_footer(text=f'r/{subreddit}')
            await ctx.send(embed=embed)
            if video:
                await ctx.send(post.url)

    @commands.command()
    async def roll(self, ctx, *, text):
        """
        Parrots your message, and adds a percentage chance to the end.
        """
        await ctx.message.delete()

        text = "".join(text)
        chance = round(random() * 100, 2)
        await ctx.send(f"{text}, {chance}%", delete_after=20)

