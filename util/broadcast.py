from util import utils


class Broadcast:
    def __init__(self, message, s):
        self.message = message
        self.seconds = s
        self.start = utils.millis()

        message1 = self.message[:16]
        message2 = self.message[:32][:-16]
        Services.screen.write_string(message1)
        Services.screen.set_cursor(0, 1)
        Services.screen.write_string(message2)

    def update(self):
        if utils.millis() - self.seconds * 1000 > self.start:
            Services.menu_manager.back(True)
