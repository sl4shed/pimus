import json

from mpv import MPV

from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from lib.services import Services
from ui.hmenu import hmenu
from ui.player import Player
from ui.vmenu import vmenu
from util.album import Album
from util.song import Song


class Artist:
    def __init__(
        self,
        id,
    ):
        self.id = id
        self.screen: Screen = Services.screen
        self.controller: Controller = Services.controller
        self.config: Config = Services.config
        self.server: Server = Services.server
        self.logger: Logger = Services.logger
        self.player: MPV = Services.player

        self.artist = self.server.get_artist(self.id)
        self.albums = self.artist["subsonic-response"]["artist"]["album"]
        self.menu = hmenu(self.artist["subsonic-response"]["artist"]["@name"])

        self.menu.add_entry(
            "Songs",
            {
                "callback": self.artist_songs,
            },
        )

        self.menu.add_entry("Albums", {"callback": self.artist_albums})

        self.menu.add_entry("Sync", {"callback": self.sync})

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()

    def artist_songs(self):
        songs = self.server.get_top_songs(
            self.artist["subsonic-response"]["artist"]["@name"]
        )

        t = vmenu("Top Songs")
        self.top_songs = []
        for i, song_obj in enumerate(songs["subsonic-response"]["topSongs"]["song"]):
            song = Song(song_obj)
            self.top_songs.append(song)
            t.add_entry(song.title, {"callback": self.select_song, "argument": i})
        Services.app.menu_manager.add(t)

    def select_song(self, i):
        t = Player(self.top_songs, i)
        Services.app.menu_manager.add(t)

    def artist_albums(self):
        menu = vmenu("Artist Albums")
        for album in self.albums:
            menu.add_entry(
                album["@name"],
                {"callback": self.select_album, "argument": album["@id"]},
            )
        Services.app.menu_manager.add(menu)
        # self.screen.clear()
        # menu.draw()

    def select_album(self, id):
        Services.app.menu_manager.add(Album(id, False))

    def sync(self):
        print("sync")
