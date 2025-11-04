from lib import lcd
from lib import control
from lib import config as configClass
from lib import server as serverClass
from lib import logger as loggerClass
from ui.progressbar import ProgressBar
from util import charmap
from util import utils
from ui import hmenu
from ui import vmenu
import time
import pygame
import mpv

from lib.bluetooth import Bluetooth
from util.album import Album
from util.playlist import Playlist
from util.settings import Settings
from util.song import Song

## Initialization ##
pygame.init()
pygame.display.set_caption("Pimus Emulator")
surface = pygame.display.set_mode((720, 130))

config = configClass.Config("./config.json")
controller = control.Controller()
screen = lcd.Screen(2, 16, charmap.charmap, 0, 0, (102, 168, 0), surface)
logger = loggerClass.Logger("./logs/pimus.log")
server = serverClass.Server(
    config.get("server.address"),
    config.get("server.username"),
    config.get("server.password"),
    "PiMus 1.0",
    logger,
)
bluetooth = Bluetooth(logger)
player = mpv.MPV()

pygame.display.flip()

## Main Loop ##
running = True
scroll = 0
global menu_history
menu_history = []


def albums():
    list = []
    albums_menu = vmenu.vmenu("Albums:", screen, controller, config)
    a = server.get_albums()
    for album in a["subsonic-response"]["albumList"]["album"]:
        albums_menu.add_entry(
            album["@name"],
            {
                "argument": album["@id"],
                "hold_argument": album["@id"],
                "hold_callback": select_album_hold,
                "callback": select_album,
            },
        )

    global menu_history
    menu_history.append(albums_menu)


def select_album(id):
    album = Album(id, False, server, controller, config, logger, screen, player)

    global menu_history
    menu_history.append(album)


def select_album_hold(id):
    album = Album(id, True, server, controller, config, logger, screen, player)

    global menu_history
    menu_history.append(album)


def artists():
    artists = server.get_artists()
    artists_alphabetic_menu = vmenu.vmenu("Artists", screen, controller, config)

    for index in artists["subsonic-response"]["artists"]["index"]:
        artists_alphabetic_menu.add_entry(
            index["@name"],
            {
                "argument": index["@name"],
                "callback": select_artist_category,
            },
        )

    global menu_history
    menu_history.append(artists_alphabetic_menu)


def select_artist_category(letter):
    artists = server.get_artists()
    artist_category_menu = vmenu.vmenu(f"Category {letter}", screen, controller, config)

    category = None
    for index in artists["subsonic-response"]["artists"]["index"]:
        if index["@name"] == letter:
            category = index

    for artist in category["artist"]:
        artist_category_menu.add_entry(
            artist["@name"], {"argument": artist["@id"], "callback": select_artist}
        )

    global menu_history
    menu_history.append(artist_category_menu)


def select_artist_hold(id):
    pass


def select_artist(id):
    pass


def search():
    pass


def options():
    menu = Settings(config, screen, controller, bluetooth)
    global menu_history
    menu_history.append(menu)


def playlists():
    list = []
    playlists_menu = vmenu.vmenu("Playlists:", screen, controller, config)
    a = server.get_playlists()
    for playlist in a["subsonic-response"]["playlists"]["playlist"]:
        playlists_menu.add_entry(
            playlist["@name"],
            {
                "argument": playlist["@id"],
                "hold_argument": playlist["@id"],
                "hold_callback": select_playlist_hold,
                "callback": select_playlist,
            },
        )

    global menu_history
    menu_history.append(playlists_menu)


def select_playlist(id):
    playlist = Playlist(id, False, server, controller, config, logger, screen, player)

    global menu_history
    menu_history.append(playlist)


def select_playlist_hold(id):
    playlist = Playlist(id, True, server, controller, config, logger, screen, player)

    global menu_history
    menu_history.append(playlist)


def select_song(song):
    pass


def go_back():
    global menu_history
    if len(menu_history) > 1:
        menu_history.pop()


main_menu = hmenu.hmenu("Pimus 1.0", screen, controller, config)
main_menu.add_entry("Playlists", {"callback": playlists})
main_menu.add_entry("Albums", {"callback": albums})
main_menu.add_entry("Artists", {"callback": artists})
main_menu.add_entry("Search", {"callback": search})
main_menu.add_entry("Options", {"callback": options})

# set the currently active menu
menu_history.append(main_menu)

while running:
    # controller update code
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    controller.update(events)

    if controller.is_repeating("left"):
        go_back()

    screen.clear()
    current_menu = menu_history[len(menu_history) - 1]
    current_menu.update()

    pygame.display.update()
    screen.draw()
