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
from lib.services import Services


class Album:
    def __init__(
        self,
        id,
        hold,
    ):
        self.id = id
        self.hold = hold
        self.server: Server = Services.server
        self.controller: Controller = Services.controller
        self.config: Config = Services.config
        self.logger: Logger = Services.logger
        self.screen: Screen = Services.screen
        self.player: Player = Services.player

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
                song = Song(song_obj)
                self.songs.append(song)

        self.menu = SongCollection(
            self.songs,
            self.album["subsonic-response"]["album"]["@name"],
            self.hold,
        )

    def update(self):
        self.menu.update()
