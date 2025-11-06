import os.path
from mpv import MPV
from lib.config import Config
from lib.logger import Logger
from lib.server import Server
from lib.services import Services


class Song:
    def __init__(self, info):
        self.info = info
        self.server: Server = Services.server
        self.config: Config = Services.config
        self.logger: Logger = Services.logger
        self.player: MPV = Services.player

        self.path = os.path.join(
            self.config.get("songs_folder"),
            self.info[
                "@path"
            ],  # this is the path that the song is stored on in the server, this way i guess you have the directory structure that you like
        )

        # metadata
        self.id = self.info["@id"]
        self.title = self.info["@title"]
        self.artist = self.info["@artist"]
        self.album = self.info["@album"]
        self.duration = int(self.info["@duration"])

        self.downloaded = os.path.exists(self.path)
        self.paused = False

    def download(self, force=False):
        if self.downloaded and not force:
            return

        self.logger.info(
            f"Downloading song {self.info['@title']} by {self.info['@artist']}"
        )
        self.server.download(self.info["@id"], self.path)

    def play(self):
        self.player.play(self.path)

    def cycle_pause(self):
        if self.paused:
            self.player.pause = False
            self.paused = False
        else:
            self.player.pause = True
            self.paused = True

        return not self.paused

    def set_volume(self, volume):
        if volume < 0:
            return
        if volume > 200:
            return
        self.player.command("set", "volume", volume)

    def get_volume(self):
        return self.player.volume
