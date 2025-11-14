from mpv import MPV

from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.logger import Logger
from lib.server import Server
from lib.services import Services
from ui.hmenu import hmenu
from ui.vmenu import vmenu
from util.album import Album


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

    def artist_songs(self):
        print("artist songs")

    def artist_albums(self):
        menu = vmenu("Artist Albums")
        Services.app.menu_manager.add(menu)
        for album in self.albums:
            self.menu.add_entry(
                album["@name"],
                {"callback": self.select_album, "argument": album["@id"]},
            )

    def select_album(self, id):
        Services.app.menu_manager.add(Album(id, False))

    def sync(self):
        print("sync")
