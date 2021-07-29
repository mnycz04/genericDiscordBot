import asyncio
import configparser
import functools
import logging
import shutil
import typing
from random import randrange

import praw
from discord import Embed, guild, member, message, utils

from Utils.mp3Downloader import Song


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, args)

    return wrapper


MAX_POSTS = 100
reddit = praw.Reddit(client_id='X0VJq7wE00FEYQ',
                     client_secret='oQ09GcBauKxPxN2su0o18Xb_EqC6vw',
                     user_agent='windows:mnycz04.discord:v1.5.3 (by /u/mnycz04; mnycz04@gmail.com)')


@to_thread
def get_mp3(query) -> (Embed, str):
    try:
        song = Song()
        song.song_query = query
        song.download_song()
        duration = f"{int(song.song_duration // 60)}:{int(song.song_duration % 60)}"

        embed = Embed(title=song.song_name, color=int(hex(int("009dff", 16)), 0))
        embed.set_image(url=song.song_thumbnail)
        embed.set_footer(text=duration)
        embed.set_author(name=song.song_url)
    except Exception as e:
        print(e)
        raise
    else:
        return embed, f"{song.song_file_location}.mp3"


default_log_format = logging.Formatter(
    "[%(name)s - %(levelname)s - %(asctime)s]: %(message)s",
    datefmt="%a %d-%b-%Y %H:%M:%S")


async def check_blacklist(server: guild, author: member):
    blacklist_role = await GuildConfig.read_config(guild_id=str(server.id),
                                                   section="ROLES",
                                                   key="blacklist_role")
    if not blacklist_role:
        return False
    blacklist_role = utils.get(server.roles, id=int(blacklist_role))
    for role in author.roles:
        if blacklist_role == role:
            return True
    return False


async def check_valid_channel(server: guild, channel_name, command: message):
    channels = set((await GuildConfig.read_config(str(server.id), section="CHANNELS", key=channel_name)).split(", "))
    logger = logging.getLogger(str(server.id))
    if channels == {''}:
        logger.info(f"Channel not set for \"{channel_name}\"")
        return True

    if str(command.channel.id) in channels:
        return True
    else:
        return False


async def check_admin(author: member):
    return author.guild_permissions.administrator


@to_thread
def get_reddit_post(query):
    subs = reddit.subreddits.search_by_name(query)

    if not subs:
        raise LookupError
    hot_posts = subs[0].hot(limit=MAX_POSTS)
    post_index = randrange(0, MAX_POSTS - 1)
    for i, post in enumerate(hot_posts):
        if i == post_index:
            submission = post

    if submission is None:
        raise ConnectionRefusedError
    else:
        return submission


class GuildConfig:
    @staticmethod
    async def read_config(guild_id: str, section: str, key: str) -> str:
        config = configparser.ConfigParser()
        try:
            config.read(f"configs/{guild_id}.ini")
            value = config.get(section, key)
        except FileNotFoundError:
            logging.getLogger(guild_id).critical(f"Config file not found for guild {guild_id}!")
            open(f"configs/{guild_id}.ini", "a").close()
            shutil.copyfile("../configs/default.ini", f"configs/{guild_id}.ini")
            return await GuildConfig.read_config(guild_id, section, key)
        except configparser.NoSectionError:
            logging.getLogger(guild_id).critical(f"Section \"{section}\" not found in {guild_id}.ini!")
            open(f"configs/{guild_id}.ini", "a").close()
            shutil.copyfile("../configs/default.ini", f"configs/{guild_id}.ini")
            return await GuildConfig.read_config(guild_id, section, key)
        except configparser.NoOptionError:
            logging.getLogger(guild_id).critical(f"Option \"{key}\" not found in section \"{section}\" in "
                                                 f"{guild_id}.ini!")
            open(f"configs/{guild_id}.ini", "a").close()
            shutil.copyfile("../configs/default.ini", f"configs/{guild_id}.ini")
            return await GuildConfig.read_config(guild_id, section, key)
        else:
            return value

    @staticmethod
    async def set_config(guild_id: str, section: str, key: str, value):
        config = configparser.ConfigParser()

        try:
            config.read(F"configs/{guild_id}.ini")
            config.set(section, key, value)
            with open(f"configs/{guild_id}.ini", "w+") as file:
                config.write(file)
        except FileNotFoundError:
            logging.getLogger(guild_id).critical(f"Config file not found for guild {guild_id}!")
            raise
        except configparser.NoSectionError:
            logging.getLogger(guild_id).critical(f"Section \"{section}\" not found in {guild_id}.ini!")
            raise
        except configparser.NoOptionError:
            logging.getLogger(guild_id).critical(f"Option \"{key}\" not found in section \"{section}\" in "
                                                 f"{guild_id}.ini!")
            raise
        finally:
            return 0
