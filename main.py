from lib import lcd
from lib import control
from util import charmap
from util import utils
from util import hmenu
from util import vmenu
import time
import pygame

## Initialization ##
pygame.init()
pygame.display.set_caption("Pimus Emulator")
surface = pygame.display.set_mode((720, 130))

controller = control.Controller()
screen = lcd.Screen(2, 16, charmap.charmap, 0, 0, (102, 168, 0), surface)
pygame.display.flip()

## Main Loop ##
running = True
scroll = 0
global active_menu
global last_menu


def albums():
    pass


def artists():
    pass


def search():
    pass


def options():
    pass


def playlists():
    playlists_menu = vmenu.vmenu("Playlists:", screen, controller)

    global active_menu
    global last_menu
    last_menu = main_menu
    active_menu = playlists_menu


def go_back():
    global active_menu
    global last_menu
    active_menu = last_menu


def select_playlist():
    print("tbm")


main_menu = hmenu.hmenu("Pimus 1.0", screen, controller)
main_menu.add_entry("Playlists", playlists)
main_menu.add_entry("Albums", albums)
main_menu.add_entry("Artists", artists)
main_menu.add_entry("Search", search)
main_menu.add_entry("Options", options)

# set the currently active menu
active_menu = main_menu
last_menu = main_menu

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
    active_menu.update()

    pygame.display.update()
    screen.draw()
