from lib.config import Config
from lib.lcd import Screen
import copy
import math


class ProgressBar:
    def __init__(self, progress, title, config: Config, screen: Screen):
        self.progress = progress
        self.title = title
        self.config = config
        self.screen = screen

        # Base characters
        self.gauge_empty = [
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_fill_1 = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_fill_2 = [
            [1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_fill_3 = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_fill_4 = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_fill_5 = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_left = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_right = [
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]

        self.gauge_mask_left = [
            [0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1],
        ]

        self.gauge_mask_right = [
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
        ]

        # Store static characters in the LCD
        self.screen.create_character(0, self.gauge_empty)
        self.screen.create_character(1, self.gauge_fill_1)
        self.screen.create_character(2, self.gauge_fill_2)
        self.screen.create_character(3, self.gauge_fill_3)
        self.screen.create_character(4, self.gauge_fill_4)
        self.screen.create_character(5, self.gauge_fill_5)

        self.gauge_size_chars = 16

    def draw(self):
        progress = max(0, min(100, self.progress))
        units_per_pixel = (self.gauge_size_chars * 5.0) / 100.0
        value_in_pixels = round(progress * units_per_pixel)

        # Determine tip positions
        tip_position = 0
        if value_in_pixels < 5:
            tip_position = 1  # left tip
        elif value_in_pixels > self.gauge_size_chars * 5 - 5:
            tip_position = 3  # right tip
        else:
            tip_position = 2  # middle

        move_offset = 4 - ((value_in_pixels - 1) % 5)

        # Dynamic left character
        gauge_left_dynamic = copy.deepcopy(self.gauge_left)
        for i in range(8):
            if tip_position == 1:
                gauge_left_dynamic[i] = (
                    self.gauge_fill_5[i][0] << move_offset
                ) | self.gauge_left[i][0:1]
            else:
                gauge_left_dynamic[i] = self.gauge_fill_5[i]
            # Apply mask
            gauge_left_dynamic[i] = [
                a & b for a, b in zip(gauge_left_dynamic[i], self.gauge_mask_left[i])
            ]
        self.screen.create_character(6, gauge_left_dynamic)

        # Dynamic right character
        gauge_right_dynamic = copy.deepcopy(self.gauge_right)
        for i in range(8):
            if tip_position == 3:
                gauge_right_dynamic[i] = (
                    self.gauge_fill_5[i][0] << move_offset
                ) | self.gauge_right[i][0:1]
            else:
                gauge_right_dynamic[i] = self.gauge_right[i]
            # Apply mask
            gauge_right_dynamic[i] = [
                a & b for a, b in zip(gauge_right_dynamic[i], self.gauge_mask_right[i])
            ]
        self.screen.create_character(7, gauge_right_dynamic)

        # Build gauge string
        gauge_chars = []
        for i in range(self.gauge_size_chars):
            if i == 0:
                gauge_chars.append(chr(6))  # dynamic left
            elif i == self.gauge_size_chars - 1:
                gauge_chars.append(chr(7))  # dynamic right
            else:
                cell_start_px = i * 5
                if value_in_pixels <= cell_start_px:
                    gauge_chars.append(chr(0))  # empty
                elif value_in_pixels >= cell_start_px + 5:
                    gauge_chars.append(chr(5))  # full
                else:
                    partial_px = value_in_pixels - cell_start_px
                    gauge_chars.append(chr(partial_px))  # 1-4

        # Draw title
        title_text = self.title[: self.gauge_size_chars].ljust(self.gauge_size_chars)
        self.screen.set_cursor(0, 0)
        self.screen.write_string(title_text)

        # Draw progress bar
        self.screen.set_cursor(0, 1)
        self.screen.write_string("".join(gauge_chars))

    def update(self):
        self.draw()

    def set_progress(self, progress):
        self.progress = progress
