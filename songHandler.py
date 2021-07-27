"""
Handles downloading and parsing of audio sources
"""

import os

import ffmpy
import youtube_dl
from requests import get

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': 'songCache/%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'default_search': 'auto',
}


class Song:

    def __init__(self):
        self.__song_query: str = ""
        self.__ytdl: object = youtube_dl.YoutubeDL(YTDL_OPTIONS)
        self.__song: object = None
        self.__song_name: str = ""
        self.__song_id: str = ""
        self.__song_file_location: str = ""
        self.__song_file_ext: str = ""
        self.__song_url: str = ""
        self.__song_duration: int = 0
        self.__song_thumbnail: str = ""

    @property
    def song_query(self) -> str:
        return self.__song_query

    @property
    def song_name(self) -> str:
        return self.__song_name

    @property
    def song_file_location(self) -> str:
        return self.__song_file_location

    @property
    def song_file_ext(self):
        return self.__song_file_ext

    @property
    def song_url(self) -> str:
        return self.__song_url

    @property
    def song_duration(self) -> int:
        return self.__song_duration

    @property
    def song_thumbnail(self):
        return self.__song_thumbnail

    @song_query.setter
    def song_query(self, query):
        self.__song_query = query
        with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
            try:
                get(query)
            except Exception:
                self.__song = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else:
                self.__song = ydl.extract_info(query, download=False)

        self.__song_name = self.__song['title']
        self.__song_id = self.__song['id']
        self.__song_file_location = f"songCache/{self.__song['id']}.{self.__song['ext']}"
        self.__song_file_ext = f"{self.__song['ext']}"
        self.__song_url = self.__song['webpage_url']
        self.__song_duration = self.__song['duration']
        self.__song_thumbnail = self.__song['thumbnail']

    async def download_song(self):
        with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ytdl:
            ytdl.download([self.__song['webpage_url']])
        ff = ffmpy.FFmpeg(inputs={f"{self.__song_file_location}": None},
                          outputs={f"songCache/{self.__song_name}.mp3": None},
                          global_options=["-y", "-loglevel error"])
        ff.run()
        os.remove(f"{self.__song_file_location}")
        self.__song_file_location = f"songCache/{self.__song_name}"
        self.__song_file_ext = "mp3"

    def __delete__(self):
        os.remove(f"{self.__song_file_location}.{self.song_file_ext}")
