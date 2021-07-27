"""
Discord Bot V3


"""

import discord
from discord.ext import commands
import os

# Sets up intents for the Bot Client
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Creates bot client, with prefix
bot = commands.Bot(command_prefix='$', intents=intents)


# Goes through all the guilds that the Bot is apart of, and ensures that a valid config file is available
@bot.event
async def on_ready():
    if bot.guilds:
        for guild in bot.guilds:
            if os.path.exists(f"logs/{guild.id}.ini"):
                print(f"Log Exists for {guild.name}")
            else:
                print(f"Log doesn't exist for {guild.name}, creating a file from \"default.ini\"")


bot.run("NzU2MzI3MDQ0MjA3NjA3OTUw.X2QOcw.MuAf1OOSi9ykYddCjETPP8uX5GM")
