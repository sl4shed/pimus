from RPLCD.i2c import CharLCD
import copy


class Screen:
    def __init__(
        self, rows, columns, charmap, x=None, y=None, color=None, surface=None
    ):  # boilerplate arguments to be able to dropin replace this from the other library
        self.lcd = CharLCD("PCF8574", 0x27, auto_linebreaks=False)
        self.columns = columns
        self.rows = rows
        self.charmap = charmap

        # i need to keep a basic state of the screen
        # to prevent redrawing shit every frame
        self.state = []
        self.custom_characters = [None] * 8
        self.cursor_x = 0
        self.cursor_y = 0
        self.false_write = False

        for r in range(0, rows):
            arr = []
            for c in range(0, columns):
                arr.append([])

            self.state.append(arr)

        self.clear()

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

        # actual code
        self.lcd.create_char(index, character)

    def set_cursor(self, x, y):
        if x > self.columns or y > self.rows or x < 0 or y < 0:
            return
        self.cursor_x = x
        self.cursor_y = y

        self.lcd.cursor_pos = (y, x)  # idk

    def write_string(self, string):
        new_state = copy.deepcopy(self.state)

        arr = list(string)
        for i, char in enumerate(arr):
            if self.cursor_x + i > self.columns:
                return

            if 0 <= ord(char) <= 7:  # characters such as \x00, \x01, etc...
                new_state[self.cursor_y][self.cursor_x + i] = self.custom_characters[
                    ord(char)
                ]
            elif ord(char) == 255:
                new_state[self.cursor_y][self.cursor_x + i] = [
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
                    new_state[self.cursor_y][self.cursor_x + i] = self.charmap.get(" ")
                else:
                    new_state[self.cursor_y][self.cursor_x + i] = self.charmap.get(char)

        if new_state != self.state:
            print("different")
            self.false_write = False
            self.state = copy.deepcopy(new_state)
            self.lcd.clear()
            self.lcd.write_string(string)
        else:
            print("same same")
            self.false_write = True

    def clear(self):
        pass

    def draw(self):
        pass
