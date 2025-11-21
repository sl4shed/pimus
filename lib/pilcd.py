from RPLCD.i2c import CharLCD
import copy


class Screen:
    def __init__(self, rows, columns, charmap, *_, **__):
        self.lcd = CharLCD("PCF8574", 0x27, auto_linebreaks=False)
        self.columns = columns
        self.rows = rows
        self.charmap = charmap

        # pixel-map state
        self.state = [[[] for _ in range(columns)] for _ in range(rows)]

        # last-known character buffer (NOT pixel maps)
        self.charbuf = [[" " for _ in range(columns)] for _ in range(rows)]

        self.custom_characters = [None] * 8
        self.cursor_x = 0
        self.cursor_y = 0

        self.dirty = True  # forces initial clear

        self.clear(force=True)

    def create_character(self, index, character):
        if 0 <= index <= 7:
            # convert 0b01010 → [0,1,0,1,0]
            if isinstance(character, (list, tuple)) and all(
                isinstance(r, int) for r in character
            ):
                converted = []
                for row in character:
                    bits = bin(row)[2:].rjust(5, "0")
                    converted.append([int(b) for b in bits])
                character = converted

            self.custom_characters[index] = character
            self.lcd.create_char(index, character)

    def set_cursor(self, x, y):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.cursor_x = x
            self.cursor_y = y
            self.lcd.cursor_pos = (y, x)

    def write_string(self, string):
        new_state = copy.deepcopy(self.state)
        new_charbuf = copy.deepcopy(self.charbuf)

        for i, char in enumerate(string):
            x = self.cursor_x + i
            y = self.cursor_y

            if x >= self.columns:
                break

            code = ord(char)

            # Update char buffer (for detecting menu changes)
            new_charbuf[y][x] = char

            # Determine pixel map
            if 0 <= code <= 7:
                # custom char
                new_state[y][x] = copy.deepcopy(self.custom_characters[code])
            elif code == 255:
                new_state[y][x] = [[1] * 5 for _ in range(8)]
            else:
                mapped = self.charmap.get(char, self.charmap.get(" "))
                new_state[y][x] = copy.deepcopy(mapped)

        # Detect pixel-level or character-level changes
        changed = new_state != self.state

        if changed:
            # If the *text* changed (menu switch, etc) → full clear
            if new_charbuf != self.charbuf:
                self.clear(force=True)

            self.state = new_state
            self.charbuf = new_charbuf
            self.lcd.write_string(string)

    def clear(self, force=False):
        if force or self.dirty:
            self.lcd.clear()
            self.lcd.cursor_pos = (self.cursor_y, self.cursor_x)
        self.dirty = False

    def draw(self):
        pass
