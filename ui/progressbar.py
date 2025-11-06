## See https://wokwi.com/projects/333991258811794002 ##

from lib.config import Config
from lib.lcd import Screen
from lib.services import Services
from util import utils


class ProgressBar:
    def __init__(self, progress, title, size=16):
        self.progress = progress
        self.title = title
        self.config: Config = Services.config
        self.screen: Screen = Services.screen
        self.gauge_size_chars = 16

        self.title_scroll = 0  # unused if the text isnt longer than the screen
        self.last_title_scroll = 0
        self.scroll_interval = self.config.get("scroll_speed")

        self.gauge_empty = (
            0b11111,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
        )
        self.gauge_fill_1 = (
            0b11111,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b11111,
        )
        self.gauge_fill_2 = (
            0b11111,
            0b11000,
            0b11000,
            0b11000,
            0b11000,
            0b11000,
            0b11000,
            0b11111,
        )
        self.gauge_fill_3 = (
            0b11111,
            0b11100,
            0b11100,
            0b11100,
            0b11100,
            0b11100,
            0b11100,
            0b11111,
        )
        self.gauge_fill_4 = (
            0b11111,
            0b11110,
            0b11110,
            0b11110,
            0b11110,
            0b11110,
            0b11110,
            0b11111,
        )
        self.gauge_fill_5 = (
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
        )
        self.gauge_left = (
            0b11111,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b11111,
        )
        self.gauge_right = (
            0b11111,
            0b00001,
            0b00001,
            0b00001,
            0b00001,
            0b00001,
            0b00001,
            0b11111,
        )
        self.gauge_mask_left = (
            0b01111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b01111,
        )
        self.gauge_mask_right = (
            0b11110,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11110,
        )

        self.gauge_mask_left = [
            0b01111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b01111,
        ]

        self.gauge_mask_right = [
            0b11110,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11110,
        ]

        self.gauge_left_dynamic = [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
        ]
        self.gauge_right_dynamic = [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
        ]

        self.screen.create_character(7, self.gauge_empty)
        self.screen.create_character(1, self.gauge_fill_1)
        self.screen.create_character(2, self.gauge_fill_2)
        self.screen.create_character(3, self.gauge_fill_3)
        self.screen.create_character(4, self.gauge_fill_4)
        # self.screen.create_character(0, self.gauge_fill_5)
        # you now have 1 empty character to put something in!!!

    def draw(self):
        units_per_pixel = (self.gauge_size_chars * 5.0) / 100.0
        value_in_pixels = round(max(1, self.progress) * units_per_pixel)

        tip_position = 0  # 0 = not set, 1 = tip in first char, 2 = tip in middle, 3 = tip in last char
        if value_in_pixels < 5:
            tip_position = 1
        elif value_in_pixels > self.gauge_size_chars * 5.0 - 5:
            tip_position = 3
        else:
            tip_position = 2

        move_offset = 4 - ((value_in_pixels - 1) % 5)

        # draw left char
        for i in range(8):
            if tip_position == 1:
                self.gauge_left_dynamic[i] = (
                    self.gauge_fill_5[i] << move_offset
                ) | self.gauge_left[i]
            else:
                self.gauge_left_dynamic[i] = self.gauge_fill_5[i]

            self.gauge_left_dynamic[i] = (
                self.gauge_left_dynamic[i] & self.gauge_mask_left[i]
            )

        # draw right char
        for i in range(8):
            if tip_position == 3:
                self.gauge_right_dynamic[i] = (
                    self.gauge_fill_5[i] << move_offset
                ) | self.gauge_right[i]
            else:
                self.gauge_right_dynamic[i] = self.gauge_right[i]

            self.gauge_right_dynamic[i] = (
                self.gauge_right_dynamic[i] & self.gauge_mask_right[i]
            )

        self.screen.create_character(5, self.gauge_left_dynamic)
        self.screen.create_character(6, self.gauge_right_dynamic)

        # "draw" progress bar
        gauge_string = []
        for i in range(self.gauge_size_chars):
            if i == 0:
                gauge_string.append("\x05")
            elif i == self.gauge_size_chars - 1:
                gauge_string.append("\x06")
            else:
                if value_in_pixels <= i * 5:
                    gauge_string.append("\x07")
                elif value_in_pixels > i * 5 and value_in_pixels < (i + 1) * 5:
                    gauge_string.append(chr(5 - move_offset))
                else:
                    # gauge_string.append("\x00")
                    gauge_string.append(chr(255))

        self.screen.set_cursor(0, 1)
        self.screen.write_string("".join(gauge_string))
        self.screen.set_cursor(0, 0)

        # title update
        if utils.millis() - self.last_title_scroll > self.scroll_interval:
            self.title_scroll += 1
            self.last_title_scroll = utils.millis()

        # Draw title
        if len(self.title) > self.screen.columns:
            utils.draw_scrolling_text(self.screen, self.title, 0, self.title_scroll)
        else:
            utils.draw_centered_text(self.screen, self.title, 0)

    def update(self):
        self.draw()

    def set_progress(self, progress):
        self.progress = progress

    def set_title(self, title):
        self.title = title
