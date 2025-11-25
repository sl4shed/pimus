import random

import pygame
from mpv import MPV

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


class SongCollection:
    def __init__(self, songs, name, hold):
        self.name = name
        self.songs = songs
        self.hold = hold
        self.server: Server = Services.server
        self.controller: Controller = Services.controller
        self.config: Config = Services.config
        self.logger: Logger = Services.logger
        self.screen: Screen = Services.screen
        self.player: Player = Services.player

        self.needs_syncing = False

        for song in songs:
            if not song.downloaded:
                self.needs_syncing = True

        if self.needs_syncing:
            self.sync()
        else:
            self.make_menu()

    def make_menu(self):
        # self.screen.clear()
        if self.hold:
            self.menu = vmenu(self.name)

            for i, song in enumerate(self.songs):
                self.menu.add_entry(
                    song.title, {"argument": i, "callback": self.select_song}
                )
        else:
            self.menu = hmenu(self.name)

            self.menu.add_entry("Play", {"argument": None, "callback": self.play})

            self.menu.add_entry("Shuffle", {"argument": None, "callback": self.shuffle})

            self.menu.add_entry("View", {"argument": None, "callback": self.view})

            self.menu.add_entry("Sync", {"argument": None, "callback": self.sync})
        self.menu.draw()

    def view(self):
        self.hold = True
        self.make_menu()

    def play(self):
        self.menu = Player(self.songs)

    def shuffle(self):
        random.shuffle(self.songs)
        self.menu = Player(self.songs)

    def sync(self, force=False):
        self.song_index = 0
        self.menu = ProgressBar(progress=0, title="Syncing...")
        self.menu.set_progress(0)
        self.needs_syncing = True
        self.force_sync = force

    def select_song(self, i):
        pass

    def update(self):
        self.menu.update()

        if isinstance(self.menu, ProgressBar) and self.needs_syncing:
            # self.menu.update()  # fix visual bug i think idk
            # pygame.time.wait(100)

            if self.song_index >= len(self.songs):
                self.make_menu()  # done syncing
                return

            progress = (100 * (self.song_index + 1)) / len(self.songs)
            self.songs[self.song_index].download(self.force_sync)
            self.menu.set_progress(progress)
            self.song_index += 1
