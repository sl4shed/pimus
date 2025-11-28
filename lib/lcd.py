import inspect
import re

print("import pygame (fuckass lcd)")
import pygame

## ts the lcd emulator!! not a real lcd class. real lcd class only works on rpi. ##
## ts code modular but not really ##


class Character:
    def __init__(self, x, y, color, surface):
        self.spacing = 0
        self.pixel_size = 7
        self.x = x
        self.y = y
        self.color = color

        self.surface = surface  # pygame

    def draw(self, map):
        for idi, i in enumerate(map):
            for idj, j in enumerate(i):
                if j == 1:
                    color = (0, 0, 0)
                else:
                    color = self.color

                pygame.draw.rect(
                    self.surface,
                    color,
                    pygame.Rect(
                        self.x + idj + idj * self.spacing + idj * self.pixel_size,
                        self.y + idi + idi * self.spacing + idi * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                    ),
                )

    def get_size(self):
        return [
            self.pixel_size * 5 + self.spacing * 5,
            self.pixel_size * 8 + self.spacing * 8,
        ]


class Screen:
    def __init__(self, rows, columns, charmap, x, y, color, surface):
        self.rows = rows
        self.columns = columns
        self.charmap = charmap
        self.custom_characters = [None] * 8
        self.cursor = [0, 0]
        self.state = []
        self.chars = []
        self.x = x
        self.y = y
        self.spacing = 10
        self.cursor_x = 0
        self.cursor_y = 0
        self.color = color
        self.surface = surface

        # initialize state and chars table
        tchar = Character(x, y, self.color, self.surface)  # 66A800
        self.char_spacing = tchar.get_size()
        for r in range(0, rows):
            arr = []
            carr = []
            for c in range(0, columns):
                arr.append([])
                character = Character(
                    self.x + self.char_spacing[0] * c + self.spacing * c,
                    self.y + self.char_spacing[1] * r + self.spacing * r,
                    self.color,
                    self.surface,
                )
                carr.append(character)

            self.state.append(arr)
            self.chars.append(carr)

        self.clear()
        self.draw()

    def create_character(self, index, character):
        if index > 7 or index < 0:
            return  # not allowed to have more than 8 chars

        if isinstance(character, (list, tuple)) and all(
            isinstance(row, int) for row in character
        ):
            # convert rows like 0b01010 -> [0,1,0,1,0]
            converted = []
            for row in character:
                bits = bin(row)[2:].rjust(5, "0")  # string like "01010"
                converted.append([int(b) for b in bits])
            character = converted

        self.custom_characters[index] = character

    def set_cursor(self, x, y):
        if x > self.columns or y > self.rows or x < 0 or y < 0:
            return
        self.cursor_x = x
        self.cursor_y = y

    def write_string(self, string):
        arr = list(string)

        for i, char in enumerate(arr):
            if self.cursor_x + i > self.columns:
                return

            if 0 <= ord(char) <= 7:  # characters such as \x00, \x01, etc...
                self.state[self.cursor_y][self.cursor_x + i] = self.custom_characters[
                    ord(char)
                ]
            elif ord(char) == 255:
                self.state[self.cursor_y][self.cursor_x + i] = [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                ]
            else:
                if not self.charmap.get(char):
                    self.state[self.cursor_y][self.cursor_x + i] = self.charmap.get(" ")
                else:
                    self.state[self.cursor_y][self.cursor_x + i] = self.charmap.get(
                        char
                    )

        self.draw()

    def draw(self):
        # draw bg
        pygame.draw.rect(
            self.surface,
            (108, 178, 1),
            pygame.Rect(
                self.x,
                self.y,
                self.char_spacing[0] * self.columns + self.spacing * self.columns,
                self.char_spacing[1] * self.rows + self.spacing * self.rows,
            ),
        )

        for idr, r in enumerate(self.chars):
            for idc, c in enumerate(r):
                c.draw(self.state[idr][idc])

    def debug_set_state(self, char, row, column):
        self.state[row][column] = char

    def clear(self):
        for idr, r in enumerate(self.state):
            for idc, c in enumerate(r):
                self.state[idr][idc] = [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                ]
