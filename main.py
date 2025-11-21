import time

import mpv
import pygame

from lib import config as configClass
from lib import control, pilcd as lcd
from lib import logger as loggerClass
from lib import server as serverClass
from lib.bluetooth import Bluetooth
from lib.services import Services
from ui import hmenu, vmenu
from ui.progressbar import ProgressBar
from util import charmap, utils
from util.album import Album
from util.artist import Artist
from util.menu_manager import MenuManager
from util.playlist import Playlist
from util.settings import Settings
from util.song import Song


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pimus Emulator")
        self.surface = pygame.display.set_mode((720, 130))
        pygame.display.flip()

        self.config = configClass.Config("./config.json")
        self.controller = control.Controller()
        self.screen = lcd.Screen(
            2, 16, charmap.charmap, 0, 0, (102, 168, 0), self.surface
        )
        self.logger = loggerClass.Logger("./logs/pimus.log")
        self.server = serverClass.Server(
            self.config.get("server.address"),
            self.config.get("server.username"),
            self.config.get("server.password"),
            "PiMus 1.0",
            self.logger,
        )
        self.bluetooth = Bluetooth(self.logger)
        self.player = mpv.MPV()

        Services.init(
            config=self.config,
            controller=self.controller,
            screen=self.screen,
            logger=self.logger,
            server=self.server,
            bluetooth=self.bluetooth,
            player=self.player,
            app=self,
        )

        self.running = True
        self.scroll = 0
        self.menu_manager = MenuManager()

        # main menu
        main_menu = hmenu.hmenu("Pimus 1.0")
        main_menu.add_entry("Playlists", {"callback": self.playlists})
        main_menu.add_entry("Albums", {"callback": self.albums})
        main_menu.add_entry("Artists", {"callback": self.artists})
        main_menu.add_entry("Search", {"callback": self.search})
        main_menu.add_entry("Options", {"callback": self.options})

        # set the currently active menu
        self.menu_manager.add(main_menu, {"backable": False})

        while self.running:
            self.update()

    def update(self):
        # controller update code
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.controller.update(events)

        if self.controller.is_repeating("left"):
            self.menu_manager.back()

        self.screen.clear()
        self.menu_manager.update()
        pygame.display.update()
        self.screen.draw()

    def albums(self):
        list = []
        albums_menu = vmenu.vmenu("Albums:")
        a = self.server.get_albums()
        for album in a["subsonic-response"]["albumList"]["album"]:
            albums_menu.add_entry(
                album["@name"],
                {
                    "argument": album["@id"],
                    "hold_argument": album["@id"],
                    "hold_callback": self.select_album_hold,
                    "callback": self.select_album,
                },
            )

        self.menu_manager.add(albums_menu)

    def select_album(self, id):
        album = Album(id, False)
        self.menu_manager.add(album)

    def select_album_hold(self, id):
        album = Album(id, True)
        self.menu_manager.add(album)

    def artists(self):
        artists = self.server.get_artists()
        artists_alphabetic_menu = vmenu.vmenu("Artists")

        for index in artists["subsonic-response"]["artists"]["index"]:
            artists_alphabetic_menu.add_entry(
                index["@name"],
                {
                    "argument": index["@name"],
                    "callback": self.select_artist_category,
                },
            )

        self.menu_manager.add(artists_alphabetic_menu)

    def select_artist_category(self, letter):
        artists = self.server.get_artists()
        artist_category_menu = vmenu.vmenu(f"Category {letter}")

        category = None
        for index in artists["subsonic-response"]["artists"]["index"]:
            if index["@name"] == letter:
                category = index

        for artist in category["artist"]:
            artist_category_menu.add_entry(
                artist["@name"],
                {
                    "argument": artist["@id"],
                    "hold_argument": artist["@id"],
                    "callback": self.select_artist,
                    "hold_callback": self.select_artist_hold,
                },
            )

        self.menu_manager.add(artist_category_menu)

    def select_artist_hold(self, id):
        pass

    def select_artist(self, id):
        artist = Artist(id)

        self.menu_manager.add(artist)

    def search(self):
        pass

    def options(self):
        menu = Settings()
        self.menu_manager.add(menu)

    def playlists(self):
        list = []
        playlists_menu = vmenu.vmenu("Playlists:")
        a = self.server.get_playlists()
        for playlist in a["subsonic-response"]["playlists"]["playlist"]:
            playlists_menu.add_entry(
                playlist["@name"],
                {
                    "argument": playlist["@id"],
                    "hold_argument": playlist["@id"],
                    "hold_callback": self.select_playlist_hold,
                    "callback": self.select_playlist,
                },
            )

        self.menu_manager.add(playlists_menu)

    def select_playlist(self, id):
        playlist = Playlist(id, False)
        self.menu_manager.add(playlist)

    def select_playlist_hold(self, id):
        playlist = Playlist(id, True)
        self.menu_manager.add(playlist)

    def select_song(self, song):
        pass


if __name__ == "__main__":
    app = App()
