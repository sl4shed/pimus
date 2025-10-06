import pygame

pygame.init()
surface = pygame.display.set_mode((400, 300))  # window


class Character:
    def __init__(self, x, y, color):
        self.spacing = 5
        self.pixel_size = 20
        self.x = x
        self.y = y
        self.color = color

        return [
            self.pixel_size * 5 + self.spacing * 5,
            self.pixel_size * 8 + self.spacing * 8,
        ]

    def draw(self, map):
        for idi, i in enumerate(map):
            for idj, j in enumerate(i):
                if j == 1:
                    color = (0, 255, 0)
                else:
                    color = self.color

                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(
                        self.x + idj + idj * self.spacing + idj * self.pixel_size,
                        self.y + idi + idi * self.spacing + idi * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                    ),
                )


class Screen:
    def __init__(self, rows, columns, charmap, x, y):
        self.rows = rows
        self.columns = columns
        self.charmap = charmap
        self.custom_characters = []
        self.cursor = [0, 0]
        self.state = []
        self.chars = []
        self.x = x
        self.y = y

        # initialize state and chars table
        for r in range(0, rows - 1):
            arr = []
            carr = []
            for c in range(0, columns - 1):
                arr.append([])
                character = Character(x, y, ())
                carr.append(character)

            self.state.append(arr)
            self.chars.append(carr)

    def set_character(self, index, character):
        if index >= 7 or index < 0:
            return  # you're not allowed to have more than 8 chars
        self.custom_characters[index] = character

    def write_string(self, string):
        pass

    def draw(self):
        pass


character = Character(30, 30, (255, 255, 255))
character.draw(
    [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
)

pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
