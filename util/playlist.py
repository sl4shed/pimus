from mpv import MPV
import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from lib.services import Services
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
    ):
        self.id = id
        self.hold = hold
        self.server: Server = Services.server
        self.controller: Controller = Services.controller
        self.config: Config = Services.config
        self.logger: Logger = Services.logger
        self.screen: Screen = Services.screen
        self.player: Player = Services.player

        self.playlist = self.server.get_playlist(id)
        self.needs_syncing = False

        self.songs = []
        for song_obj in self.playlist["subsonic-response"]["playlist"]["entry"]:
            song = Song(song_obj)
            self.songs.append(song)
            if not song.downloaded:
                self.needs_syncing = True  # if even ONE song isnt downloaded, the playlist needs syncing.

        self.menu = SongCollection(
            self.songs,
            self.playlist["subsonic-response"]["playlist"]["@name"],
            self.hold,
        )

    def update(self):
        self.menu.update()
