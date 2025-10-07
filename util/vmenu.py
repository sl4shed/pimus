from util import utils


class vmenu:
    def __init__(self, title, screen, controller):
        self.title = title
        self.screen = screen
        self.controller = controller
        self.entries = []

        self.entry_index = 0
        self.cursor_y = 0
        self.active_y = 0
        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = 100

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

    def add_entry(self, text, callback):
        self.entries.append({"text": text, "callback": callback})

    def update(self):
        # title update
        if utils.millis() - self.last_title_scroll > self.scroll_interval:
            self.title_scroll += 1
            self.last_title_scroll = utils.millis()

        # controller
        if self.controller.just_pressed("down"):
            if self.entry_index + 2 > len(self.entries):
                return
            if self.cursor_y == 0:
                self.cursor_y = 1
            elif self.cursor_y == 1:
                self.active_y = 1
                self.entry_index += 1
        elif self.controller.just_pressed("up"):
            if self.entry_index - 2 < 0:
                return
            if self.cursor_y == 0:
                self.active_y = 1
                self.entry_index -= 1
            elif self.cursor_y == 1:
                self.cursor_y = 0
        elif self.controller.just_pressed("select"):
            self.entries[self.entry_index]["callback"]()

        self.draw()

    def draw_entry(self, entry, row):
        if len(entry["text"]) > self.screen.columns - 1:
            utils.draw_boundary_scrolling_text(
                self.screen, entry["text"], row, 1, 15, self.title_scroll
            )
        else:
            self.screen.set_cursor(1, row)
            self.screen.write_string(entry["text"])

    def draw(self):
        if self.active_y == 0:
            self.screen.set_cursor(0, 0)
            entry = self.entries[self.entry_index]
            self.draw_entry(entry, 0)

            if len(self.entries) > 0:
                self.screen.set_cursor(0, 1)
                entry = self.entries[self.entry_index + 1]
                self.draw_entry(entry, 1)
        elif self.active_y == 1:
            self.screen.set_cursor(0, 1)
            entry = self.entries[self.entry_index]
            self.draw_entry(entry, 1)

            if self.entry_index > 0:
                self.screen.set_cursor(0, 0)
                entry = self.entries[self.entry_index - 1]
                self.draw_entry(entry, 0)

        self.screen.set_cursor(0, self.cursor_y)
        self.screen.write_string(">")

        if self.entry_index + 1 < len(self.entries):
            self.screen.set_cursor(self.screen.columns - 1, 1)
            self.screen.write_string("\x00")
        if self.entry_index - 1 > 0:
            self.screen.set_cursor(self.screen.columns - 1, 0)
            self.screen.write_string("\x01")
