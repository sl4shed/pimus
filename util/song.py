import os.path
from lib.config import Config
from lib.logger import Logger
from lib.server import Server
import mpv
import pygame


class Song:
    def __init__(self, info, config: Config, server: Server, logger: Logger, player):
        self.info = info
        self.server = server
        self.config = config
        self.logger = logger
        self.player = player

        self.path = os.path.join(
            self.config.get("songs_folder"),
            self.info[
                "@path"
            ],  # this is the path that the song is stored on in the server, this way i guess you have the directory structure that you like
        )

        # print(self.info)

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
        # pygame.mixer.music.load(self.path)
        # pygame.mixer.music.play()

    def cycle_pause(self):
        if self.paused:
            self.player.command("keypress", "SPACE")
            self.paused = False
        else:
            self.player.command("keypress", "SPACE")
            self.paused = True

        return not self.paused

    def increase_volume(self):
        self.player.command("keypress", "*")

    def decrease_volume(self):
        self.player.command("keypress", "/")

    def set_volume(self, volume):
        self.player.command("set", "volume", volume)

    def get_volume(self):
        return self.player.observe_property("volume")
