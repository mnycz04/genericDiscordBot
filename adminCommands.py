import logging

from discord import utils
from discord.ext import commands

from utilities import GuildConfig, check_admin, check_valid_channel


class AdminCommands(commands.Cog, name="Administrator Commands"):
    """Commands that require Admin tags to use"""

    @commands.command()
    async def setmusic(self, ctx):
        """
        Sets music channel, where music related commands will work in
        """
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.author):
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
        """
        Sets embed channel, where $reddit will only work in
        """
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setembed command, but was denied.")
            return None

        current_embed_channels = set((await GuildConfig
                                     .read_config(str(ctx.guild.id),
                                                  "CHANNELS",
                                                  "embed_channel"))
                                     .split(", "))
        for item in current_embed_channels:
            if not item:
                current_embed_channels.remove(item)
                break

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
        """
        Sets the admin channel, where some commands can only be used
        """
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.author):
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
    async def setann(self, ctx):
        """
        Sets the announcements channel, where announcements will be sent
        """
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setann command, but was denied.")
            return None

        current_announcements_channel = await GuildConfig.read_config(str(ctx.guild.id), "CHANNELS",
                                                                      "announcements_channel")
        if str(ctx.message.channel.id) == current_announcements_channel:
            await GuildConfig.set_config(str(ctx.guild.id), section="CHANNELS", key="announcements_channel", value="")
            logger.info("announcements channel restriction deleted.")
            await ctx.send("announcements Channels Restriction removed.", delete_after=10)
        else:
            await GuildConfig.set_config(str(ctx.guild.id),
                                         section="CHANNELS",
                                         key="announcements_channel",
                                         value=str(ctx.message.channel.id))
            logger.info(f"Set announcements channel to {ctx.message.channel.id}")
            await ctx.send("announcements Channel Set!", delete_after=10)

    @commands.command()
    async def setbl(self, ctx, role: str):
        """
        Sets the blacklist role, who can't use member commands
        """
        logger = logging.getLogger(str(ctx.guild.id))
        await ctx.message.delete()

        if not await check_admin(ctx.author):
            await ctx.send("You don't have permission to use that command!")
            logger.info(f"{ctx.author.name} tried to use setbl command, but was denied.")
            return None
        role = role.strip("<>!@&")
        current_blacklist_role = await GuildConfig.read_config(str(ctx.guild.id), "ROLES", "blacklist_role")
        if current_blacklist_role == role:
            await GuildConfig.set_config(str(ctx.guild.id), "ROLES", "blacklist_role", "")
            logger.info(f"{ctx.author.name} removed blacklist role")
            await ctx.send("Removed Blacklist Role", delete_after=10)
            return
        else:
            await GuildConfig.set_config(str(ctx.guild.id), "ROLES", "blacklist_role", role)
            await ctx.send('Changed blacklist role.', delete_after=10)
            logger.info(f"{ctx.author.name} changed the blacklist role to {role}")

    @commands.command()
    async def announce(self, ctx):
        """
        Makes an announcement, must set-up a channel with $setann
        """
        await ctx.message.delete()
        logger = logging.getLogger(str(ctx.guild.id))
        if await check_admin(ctx.author):
            pass
        else:
            await ctx.send('You don\'t have the permissions for that!', delete_after=5)
            logger.info(f"{ctx.author.name} tried to announce something")

        if not check_valid_channel(ctx.guild, ctx.channel.name, "announcements_channel"):
            await ctx.send("Invalid Channel. Unable to send")
            return
        if await GuildConfig.read_config(str(ctx.guild.id), "CHANNELS", "announcements_channel") != "":
            announcements_channel = int(await GuildConfig.read_config(str(ctx.guild.id),
                                                                      "CHANNELS",
                                                                      "announcements_channel"))
        announcements_channel = utils.get(ctx.guild.channels, id=announcements_channel)
        if str(ctx.message.content)[9:] == "":
            return
        await announcements_channel.send(str(ctx.message.content)[9:])
        logger.info(f"{ctx.author.name} sent an announcement")
