import os.path

import pygame


class Song:
    def __init__(self, info, config, server, logger):
        self.info = info
        self.server = server
        self.config = config
        self.logger = logger

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
        print(f"tryna play {self.path}")
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()

    def cycle_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

        return not self.paused
