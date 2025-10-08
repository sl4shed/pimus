from util import utils


class hmenu:
    def __init__(self, title, screen, controller, config):
        self.title = title
        self.entries = []

        self.screen = screen
        self.controller = controller
        self.config = config

        self.entry_index = 0
        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = self.config.get("scroll_speed")

    def add_entry(self, text, callback):
        self.entries.append({"text": text, "callback": callback})

    def update(self):
        # title update
        if utils.millis() - self.last_title_scroll > self.scroll_interval:
            self.title_scroll += 1
            self.last_title_scroll = utils.millis()

        # selection updating
        if self.controller.just_pressed("select"):
            self.entries[self.entry_index]["callback"]()

        if (
            self.controller.just_pressed("right")
            and self.entry_index < len(self.entries) - 1
        ):
            self.entry_index += 1

        if self.controller.just_pressed("left") and self.entry_index > 0:
            self.entry_index -= 1

        self.draw()

    def draw(self):
        if len(self.title) > self.screen.columns:
            utils.draw_scrolling_text(self.screen, self.title, 0, self.title_scroll)
        else:
            utils.draw_centered_text(self.screen, self.title, 0)

        if self.entry_index != 0:
            self.screen.set_cursor(0, 1)
            self.screen.write_string("<")

        if self.entry_index != len(self.entries) - 1:
            self.screen.set_cursor(self.screen.columns - 1, 1)
            self.screen.write_string(">")

        current_entry = self.entries[self.entry_index]
        if len(current_entry["text"]) > self.screen.columns - 2:
            utils.draw_boundary_scrolling_text(
                self.screen, current_entry["text"], 1, 1, 15, self.title_scroll
            )
        else:
            utils.draw_centered_text(self.screen, current_entry["text"], 1)
