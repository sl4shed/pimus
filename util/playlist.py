from mpv import MPV
import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from ui.hmenu import hmenu
from ui.player import Player
from ui.progressbar import ProgressBar
from ui.vmenu import vmenu
from util.song import Song
from util.song_collection import SongCollection


class Playlist:
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

        self.playlist = self.server.get_playlist(id)
        self.needs_syncing = False

        self.songs = []
        for song_obj in self.playlist["subsonic-response"]["playlist"]["entry"]:
            song = Song(song_obj, self.config, self.server, self.logger, self.player)
            self.songs.append(song)
            if not song.downloaded:
                self.needs_syncing = True  # if even ONE song isnt downloaded, the playlist needs syncing.

        print(self.playlist)
        self.menu = SongCollection(
            self.songs,
            self.playlist["subsonic-response"]["playlist"]["@name"],
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
