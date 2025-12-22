from RPLCD.i2c import CharLCD
import copy


class Screen:
    def __init__(
        self, rows, columns, charmap, x=None, y=None, color=None, surface=None
    ):  # boilerplate arguments to be able to dropin replace this from the other library
        self.lcd = CharLCD("PCF8574", 0x27, auto_linebreaks=False)
        self.columns = columns
        self.rows = rows
        self.cursor_x = 0
        self.cursor_y = 0

        self.lcd.clear()
        self.lcd.write_string("pepe")

    def create_character(self, index, character):
        if index > 7 or index < 0:
            return  # not allowed to have more than 8 chars

        # actual code
        self.lcd.create_char(index, character)

    def set_cursor(self, x, y):
        if x > self.columns or y > self.rows or x < 0 or y < 0:
            return
        self.cursor_x = x
        self.cursor_y = y

        self.lcd.cursor_pos = (y, x)  # idk

    def write_string(self, string):
        self.lcd.write_string(string)

    def clear(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (self.cursor_y, self.cursor_x)  # retain cursor pos

    def draw(self):
        pass
