from time import sleep
from util import utils


class hmenu:
    def __init__(self, title, screen, controller):
        self.title = title
        self.entries = []
        self.screen = screen
        self.controller = controller

        self.entry_index = 0
        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = 100

        self.screen.create_character(
            0,
            [
                [0, 0, 0, 0, 1],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
            ],
        )

        self.screen.create_character(
            1,
            [
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        )

    def add_entry(self, text, callback):
        self.entries.append({"text": text, "callback": callback})

    def update(self):
        # title update
        if (
            len(self.title) > self.screen.columns
            and utils.millis() - self.last_title_scroll > self.scroll_interval
        ):
            self.title_scroll += 1
            self.last_title_scroll = utils.millis()

        # selection updating

        self.draw()

    def draw(self):
        if len(self.title) > self.screen.columns:
            utils.draw_scrolling_text(self.screen, self.title, 0, self.title_scroll)
        else:
            utils.draw_centered_text(self.screen, self.title, 0)

        if self.entry_index != 0:
            self.screen.set_cursor(0, 1)
            self.screen.write_string("\x00")

        if self.entry_index != len(self.entries):
            self.screen.set_cursor(self.screen.columns - 1, 1)
            self.screen.write_string("\x01")
