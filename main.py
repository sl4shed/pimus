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


def playlists():
    print("pula")


def albums():
    pass


def artists():
    pass


def search():
    pass


def options():
    pass


# menu = hmenu.hmenu("Pimus 1.0", screen, controller)
# menu.add_entry("Playlists", playlists)  # hmenu
# menu.add_entry("Albums", albums)  # vmenu
# menu.add_entry("Artists", artists)  # vmenu
# menu.add_entry("Search", search)  # not yet implemented
# menu.add_entry("Options", options)  # hmenu

menu2 = vmenu.vmenu("Playlists:", screen, controller)
menu2.add_entry("The j", playlists)
menu2.add_entry("Test Entry With Long Title", playlists)
menu2.add_entry("Bla bla", playlists)
menu2.add_entry("Another Long Entry", playlists)
menu2.add_entry("New Playlist", playlists, True)

while running:
    # controller update code
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    controller.update(events)

    screen.clear()
    # menu.update()
    menu2.update()

    pygame.display.update()
    screen.draw()
