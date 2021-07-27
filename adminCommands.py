import discord
from discord.ext import commands
import logging

from utilities import GuildConfig, check_admin


class AdminCommands(commands.Cog, name="Administrator Commands"):
    """Commands that require Admin tags to use"""

    @commands.command()
    async def setmusic(self, ctx):
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.guild, ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setmusic command, but was denied.")
            return None

        current_music_channel = await GuildConfig.read_config(str(ctx.guild.id), "CHANNELS", "music_cmds_channel")
        if str(ctx.message.channel.id) == current_music_channel:
            await GuildConfig.set_config(str(ctx.guild.id), section="CHANNELS", key="music_cmds_channel", value="")
            logger.info("Music channel restriction deleted.")
            await ctx.send("Music Channels Restriction removed.", delete_after=10)
        else:
            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="music_cmds_channel",
                                         value=str(ctx.message.channel.id))
            logger.info(f"Set music channel to {ctx.message.channel.id}")
            await ctx.send("Music Channel Set!", delete_after=10)

    @commands.command()
    async def setembed(self, ctx):
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.guild, ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setembed command, but was denied.")
            return None

        current_embed_channels = set((await GuildConfig
                                      .read_config(str(ctx.guild.id),
                                                   "CHANNELS",
                                                   "embed_channel"))
                                     .split(", "))
        if str(ctx.message.channel.id) in current_embed_channels:
            current_embed_channels.remove(str(ctx.message.channel.id))
            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="embed_channel",
                                         value=", ".join(current_embed_channels))
            logger.info(f"Embed channel restriction deleted for {ctx.message.channel.id}.")
            await ctx.send("Embed Channels Restriction removed.", delete_after=10)
        else:
            current_embed_channels.add(str(ctx.message.channel.id))

            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="embed_channel",
                                         value=", ".join(current_embed_channels))
            logger.info(f"Set an embed channel to {ctx.message.channel.id}")
            await ctx.send("Embed Channel Set!", delete_after=10)

    @commands.command()
    async def setadmin(self, ctx):
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.guild, ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setadmin command, but was denied.")
            return None

        current_music_channel = await GuildConfig.read_config(str(ctx.guild.id), "CHANNELS", "admin_channel")
        if str(ctx.message.channel.id) == current_music_channel:
            await GuildConfig.set_config(str(ctx.guild.id), section="CHANNELS", key="admin_channel", value="")
            logger.info("Admin channel restriction deleted.")
            await ctx.send("Admin Channels Restriction removed.", delete_after=10)
        else:
            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="admin_channel",
                                         value=str(ctx.message.channel.id))
            logger.info(f"Set admin channel to {ctx.message.channel.id}")
            await ctx.send("Admin Channel Set!", delete_after=10)

    @commands.command()
    async def setbl(self, ctx):
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.guild, ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setbl command, but was denied.")
            return None

        current_music_channel = await GuildConfig.read_config(str(ctx.guild.id), "CHANNELS", "admin_channel")
        if str(ctx.message.channel.id) == current_music_channel:
            await GuildConfig.set_config(str(ctx.guild.id), section="CHANNELS", key="admin_channel", value="")
            logger.info("Admin channel restriction deleted.")
            await ctx.send("Admin Channels Restriction removed.", delete_after=10)
        else:
            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="admin_channel",
                                         value=str(ctx.message.channel.id))
            logger.info(f"Set admin channel to {ctx.message.channel.id}")
            await ctx.send("Admin Channel Set!", delete_after=10)

