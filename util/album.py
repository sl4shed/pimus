from mpv import MPV
import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from ui.player import Player
from ui.progressbar import ProgressBar
from util.song import Song
from util.song_collection import SongCollection


class Album:
    def __init__(
        self,
        id,
        hold,
        server: Server,
        controller: Controller,
        config: Config,
        logger: Logger,
        screen: Screen,
        player: MPV,
    ):
        self.id = id
        self.hold = hold
        self.server = server
        self.controller = controller
        self.config = config
        self.logger = logger
        self.screen = screen
        self.player = player

        self.album = self.server.get_album(id)
        self.needs_syncing = False

        self.songs = []

        if not isinstance(self.album["subsonic-response"]["album"]["song"], list):
            song = Song(
                self.album["subsonic-response"]["album"]["song"],
                self.config,
                self.server,
                self.logger,
                self.player,
            )
            self.songs.append(song)
        else:
            for song_obj in self.album["subsonic-response"]["album"]["song"]:
                song = Song(
                    song_obj, self.config, self.server, self.logger, self.player
                )
                self.songs.append(song)

        self.menu = SongCollection(
            self.songs,
            self.album["subsonic-response"]["album"]["@name"],
            self.hold,
            self.server,
            self.controller,
            self.config,
            self.logger,
            self.screen,
            self.player,
        )

    def update(self):
        self.menu.update()
