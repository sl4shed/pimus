import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from ui.hmenu import hmenu
from ui.progressbar import ProgressBar
from ui.vmenu import vmenu
from util.song import Song


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
    ):
        self.id = id
        self.hold = hold
        self.server = server
        self.controller = controller
        self.config = config
        self.logger = logger
        self.screen = screen

        self.playlist = self.server.get_playlist(id)
        self.needs_syncing = False

        self.songs = []
        for song_obj in self.playlist["subsonic-response"]["playlist"]["entry"]:
            song = Song(song_obj, self.config, self.server, self.logger)
            self.songs.append(song)
            if not song.downloaded:
                self.needs_syncing = True  # if even ONE song isnt downloaded, the playlist needs syncing.

        if self.needs_syncing:
            self.sync()
        else:
            self.make_playlist_menu()

    def make_playlist_menu(self):
        if self.hold:
            self.menu = vmenu(
                self.playlist["subsonic-response"]["playlist"]["@name"],
                self.screen,
                self.controller,
                self.config,
            )

            for i, song in enumerate(self.songs):
                self.menu.add_entry(
                    song.title, {"argument": i, "callback": self.select_song}
                )
        else:
            self.menu = hmenu(
                self.playlist["subsonic-response"]["playlist"]["@name"],
                self.screen,
                self.controller,
                self.config,
            )

            self.menu.add_entry("Play", {"argument": None, "callback": self.play})

            self.menu.add_entry("Shuffle", {"argument": None, "callback": self.shuffle})

            self.menu.add_entry("Sync", {"argument": None, "callback": self.sync})

    def play(self):
        pass

    def shuffle(self):
        pass

    def sync(self):
        self.song_index = 0
        self.menu = ProgressBar(
            progress=0, title="Syncing...", config=self.config, screen=self.screen
        )
        self.needs_syncing = True

    def select_song(self, i):
        song = self.songs[i]
        pygame.mixer.music.load(song.path)
        pygame.mixer.music.play()

    def update(self):
        self.menu.update()

        if isinstance(self.menu, ProgressBar):  # syncing
            if self.song_index >= len(self.songs):
                self.make_playlist_menu()  # done syncing
                return

            progress = (100 * (self.song_index + 1)) / len(self.songs)
            self.songs[self.song_index].download()
            self.menu.set_progress(progress)
            self.song_index += 1
