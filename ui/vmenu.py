from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from util import utils
from lib.services import Services


class vmenu:
    def __init__(self, title):
        self.title = title
        self.screen: Screen = Services.screen
        self.controller: Controller = Services.controller
        self.config: Config = Services.config
        self.entries = []

        self.entry_index = 0
        self.cursor = 1
        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = self.config.get("scroll_speed")

        self.screen.create_character(
            0,
            [
                0b00000,
                0b00000,
                0b00000,
                0b00000,
                0b11111,
                0b01110,
                0b00100,
                0b00000,
            ],
        )

        self.screen.create_character(
            1,
            [
                0b00000,
                0b00100,
                0b01110,
                0b11111,
                0b00000,
                0b00000,
                0b00000,
                0b00000,
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

        if not hasattr(self, "creation_time"):
            self.creation_time = utils.millis()
            self.input_cooldown = 200  # ms

        if self.entries[self.entry_index]["options"].get("selectable", None) == False:
            self.cursor = 1

        # Cooldown to prevent instant selection from previous menu
        if utils.millis() - self.creation_time < self.input_cooldown:
            self.draw()
            return

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

        elif self.controller.just_held("select"):
            idx = self.entry_index + self.cursor
            if 0 <= idx < len(self.entries):
                entry = self.entries[idx]
                if entry["options"].get("hold_callback", None):
                    if entry["options"].get("hold_argument", None):
                        entry["options"]["hold_callback"](
                            entry["options"]["hold_argument"]
                        )
                    else:
                        entry["options"]["hold_callback"]()

        elif self.controller.is_click("select"):
            idx = self.entry_index + self.cursor
            if 0 <= idx < len(self.entries):
                entry = self.entries[idx]
                if entry["options"].get("callback", None):
                    if entry["options"].get("argument", None):
                        entry["options"]["callback"](entry["options"]["argument"])
                    else:
                        entry["options"]["callback"]()

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
