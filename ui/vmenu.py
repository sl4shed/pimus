from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from util import utils


class vmenu:
    def __init__(self, title, screen: Screen, controller: Controller, config: Config):
        self.title = title
        self.screen = screen
        self.controller = controller
        self.config = config
        self.entries = []

        self.entry_index = 0
        self.cursor = 1
        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = self.config.get("scroll_speed")

        self.screen.create_character(
            0,
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        )

        self.screen.create_character(
            1,
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        )

        self.add_entry(
            self.title, {"centered": True, "selectable": False, "callback": None}
        )

    def add_entry(self, text, options):
        self.entries.append({"text": text, "options": options})

    def update(self):
        # title update
        if utils.millis() - self.last_title_scroll > self.scroll_interval:
            self.title_scroll += 1
            self.last_title_scroll = utils.millis()

        if self.entries[self.entry_index]["options"].get("selectable", None) == False:
            self.cursor = 1

        # controller stuff
        if self.controller.just_pressed("down"):
            # if cursor is on top row and theres another entry below just move it down
            if self.cursor == 0 and self.entry_index + 1 < len(self.entries):
                self.cursor = 1
            # if cursor already on bottom row scroll down (if possible)
            elif self.cursor == 1 and self.entry_index + 1 < len(self.entries) - 1:
                self.entry_index += 1

        elif self.controller.just_pressed("up"):
            # if cursor is on bottom row, move it up
            if self.cursor == 1:
                self.cursor = 0
            # if cursor is already at top and we can scroll up
            elif self.cursor == 0 and self.entry_index > 0:
                self.entry_index -= 1

        elif self.controller.just_released("select"):
            idx = self.entry_index + self.cursor
            if 0 <= idx < len(self.entries):
                if self.entries[idx]["options"].get("argument", None):
                    self.entries[idx]["options"]["callback"](
                        self.entries[idx]["options"]["argument"]
                    )
                else:
                    self.entries[idx]["options"]["callback"]()
        elif self.controller.is_repeating("select"):
            idx = self.entry_index + self.cursor
            if 0 <= idx < len(self.entries):
                if not self.entries[idx]["options"].get("hold_callback", None):
                    return
                if self.entries[idx]["options"].get("hold_argument", None):
                    self.entries[idx]["options"]["hold_callback"](
                        self.entries[idx]["options"]["hold_argument"]
                    )
                else:
                    self.entries[idx]["options"]["hold_callback"]()

        self.draw()

    def draw_entry(self, entry, row):
        if len(entry["text"]) > self.screen.columns - 1:
            utils.draw_boundary_scrolling_text(
                self.screen, entry["text"], row, 1, 15, self.title_scroll
            )
        else:
            if entry["options"].get("centered", False):
                utils.draw_centered_text(self.screen, entry["text"], row)
            else:
                self.screen.set_cursor(1, row)
                self.screen.write_string(entry["text"])

    def draw(self):
        top_index = self.entry_index
        bottom_index = top_index + 1

        # top entry
        if top_index < len(self.entries):
            self.screen.set_cursor(1, 0)
            self.draw_entry(self.entries[top_index], 0)

        # bottom entry
        if bottom_index < len(self.entries):
            self.screen.set_cursor(1, 1)
            self.draw_entry(self.entries[bottom_index], 1)

        # cursor
        self.screen.set_cursor(0, self.cursor)
        self.screen.write_string(">")

        # up/down indicators
        if top_index > 0:
            self.screen.set_cursor(self.screen.columns - 1, 0)
            self.screen.write_string("\x01")
        if bottom_index < len(self.entries) - 1:
            self.screen.set_cursor(self.screen.columns - 1, 1)
            self.screen.write_string("\x00")
