import asyncio
import configparser
import functools
import logging
import typing

from discord import Embed, guild, member, message, utils

from songHandler import Song


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, func, args)

    return wrapper


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
    blacklist_role = utils.get(server.roles, id=int(blacklist_role))
    for role in author.roles:
        if blacklist_role == role:
            return True
    return False


async def check_valid_channel(server: guild, channel_name, command: message):
    channel = await GuildConfig.read_config(str(server.id), section="CHANNELS", key=channel_name)
    if channel == "":
        return True

    if int(channel) == command.channel.id:
        return True
    else:
        return False


async def check_admin(server: guild, author: member):
    return author.guild_permissions.administrator


class GuildConfig:

    @staticmethod
    async def read_config(guild_id: str, section: str, key: str) -> str:
        config = configparser.ConfigParser()
        try:
            config.read(f"configs/{guild_id}.ini")
            value = config.get(section, key)
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
