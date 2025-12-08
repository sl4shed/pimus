import asyncio
from time import sleep

from lib.services import Services
from util import utils


class Broadcast:
    async def __init__(self, message, s, app):
        self.message = message
        self.seconds = s
        self.start = utils.millis()
        self.app = app

        message1 = self.message[:16]
        message2 = self.message[:32][:-16]
        self.app.screen.write_string(message1)
        self.app.screen.set_cursor(0, 1)
        self.app.screen.write_string(message2)
        await asyncio.sleep(0.02)
        sleep(1)
        return None  # i give up

    def update(self):
        if utils.millis() - 20 > self.start:
            self.app.menu_manager.back(True)
