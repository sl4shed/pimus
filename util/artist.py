from mpv import MPV
from lib import logger
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.server import Server
from ui.hmenu import hmenu
from ui.vmenu import vmenu
from util.album import Album


class Artist:
    def __init__(
        self,
        id,
        server: Server,
        screen: Screen,
        controller: Controller,
        config: Config,
        logger: logger.Logger,
        player: MPV,
    ):
        self.id = id
        self.screen = screen
        self.controller = controller
        self.config = config
        self.server = server
        self.logger = logger
        self.player = player

        self.artist = self.server.get_artist(self.id)
        self.albums = self.artist["subsonic-response"]["artist"]["album"]

        self.menu = hmenu(
            self.artist["subsonic-response"]["artist"]["@name"],
            self.screen,
            self.controller,
            self.config,
        )

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
        self.menu = vmenu("Artist Albums", self.screen, self.controller, self.config)
        for album in self.albums:
            self.menu.add_entry(
                album["@name"],
                {"callback": self.select_album, "argument": album["@id"]},
            )

    def select_album(self, id):
        self.menu = Album(
            id,
            False,
            self.server,
            self.controller,
            self.config,
            self.logger,
            self.screen,
            self.player,
        )

    def sync(self):
        print("sync")
