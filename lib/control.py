import pygame
import time
# emulator class


class Controller:
    def __init__(self):
        self.current_state = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "select": False,
        }

        self.previous_state = {key: False for key in self.current_state}

        self.press_time = {key: float(0) for key in self.current_state}
        self.repeat_delay = 0.5
        self.repeat_rate = 0.15

        self.key_map = {
            pygame.K_UP: "up",
            pygame.K_w: "up",
            pygame.K_DOWN: "down",
            pygame.K_s: "down",
            pygame.K_LEFT: "left",
            pygame.K_a: "left",
            pygame.K_RIGHT: "right",
            pygame.K_d: "right",
            pygame.K_RETURN: "select",
            pygame.K_SPACE: "select",
        }

    def update(self, events):
        current_time = time.time()

        self.previous_state = self.current_state.copy()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_map:
                    button = self.key_map[event.key]
                    self.current_state[button] = True
                    self.press_time[button] = current_time

            elif event.type == pygame.KEYUP:
                if event.key in self.key_map:
                    button = self.key_map[event.key]
                    self.current_state[button] = False

    def is_pressed(self, button):
        return self.current_state[button]

    def just_pressed(self, button):
        return self.current_state[button] and not self.previous_state[button]

    def just_released(self, button):
        return not self.current_state[button] and self.previous_state[button]

    def is_repeating(self, button):
        if not self.current_state[button]:
            return False

        held_time = time.time() - self.press_time[button]

        if held_time < self.repeat_delay:
            return False

        time_since_initial = held_time - self.repeat_delay
        return int(time_since_initial / self.repeat_rate) > int(
            (time_since_initial - 0.016) / self.repeat_rate
        )
