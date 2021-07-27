"""
Discord Bot V3


"""

import logging
import os
from shutil import copyfile

import discord
from discord.ext import commands

from adminCommands import AdminCommands
from memberCommands import MemberCommands
from utilities import default_log_format

# Sets up intents for the Bot Client
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Creates bot client, with prefix
bot = commands.Bot(command_prefix='$', intents=intents)

# Checks if 'logs' Directory exists, if it doesn't, it'll make it
if not os.path.exists("logs/"):
    os.mkdir("logs/")
    print("Created Logs Directory")

discord_logger = logging.getLogger("discord")
_file_handler = logging.FileHandler("logs/discord.log", encoding="utf-8", mode="w")
_file_handler.setFormatter(default_log_format)
discord_logger.addHandler(_file_handler)
_console_handler = logging.StreamHandler()
_console_handler.setFormatter(default_log_format)
discord_logger.addHandler(_console_handler)
discord_logger.setLevel(20)


@bot.event
async def on_ready():
    # Checks for Server Specific Config Files, creates new ones if necessary
    for guild in bot.guilds:
        try:
            if not os.path.exists(f"configs/{guild.id}.ini"):
                raise FileNotFoundError
            discord_logger.info(f"Found .ini for Guild: {guild.id}")
        except FileNotFoundError:
            discord_logger.info(f"Creating .ini for Guild: {guild.id}")
            try:
                if not os.path.exists(f"configs/default.ini"):
                    raise FileNotFoundError()
                open(f"configs/{guild.id}.ini", "a").close()
                copyfile("configs/default.ini", f"configs/{guild.id}.ini")
            except FileNotFoundError:
                quit(discord_logger.fatal('"configs/default.ini" not found.'))
    for guild in bot.guilds:
        guild_log = logging.getLogger(str(guild.id))
        _file = logging.FileHandler(f"logs/{guild.id}.log")
        _file.setFormatter(default_log_format)
        guild_log.addHandler(_file)
        guild_log.setLevel(20)
        strout = logging.StreamHandler()
        strout.setFormatter(default_log_format)
        guild_log.addHandler(strout)


bot.add_cog(MemberCommands())
bot.add_cog(AdminCommands())
bot.run("NzU2MzI3MDQ0MjA3NjA3OTUw.X2QOcw.MuAf1OOSi9ykYddCjETPP8uX5GM")
