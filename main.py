from lib import lcd
from lib import control
from util import charmap
from util import utils
from util import hmenu
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
menu = hmenu.hmenu("the quick brown fox jumps over the lazy dog.", screen, controller)
while running:
    # controller update code
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    controller.update(events)

    screen.clear()
    menu.update()

    pygame.display.update()
    screen.draw()
