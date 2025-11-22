import time
import sys
import select

class Controller:
    def __init__(self):
        self.current_state = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "select": False,
        }

        self.previous_state = self.current_state.copy()

        self.press_time = {k: 0.0 for k in self.current_state}

        self.repeat_delay = 0.5
        self.repeat_rate = 0.15

        self.hold_duration = 0.5
        self.hold_triggered = {k: False for k in self.current_state}
        self.prev_hold_triggered = self.hold_triggered.copy()

    def _read_console(self):
        """
        Non-blocking read from stdin.
        Returns a line or None.
        """
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.readline().strip()
        return None

    def update(self):
        current_time = time.time()

        # copy previous state
        self.previous_state = self.current_state.copy()
        self.prev_hold_triggered = self.hold_triggered.copy()

        # read input
        line = self._read_console()

        if line:
            parts = line.lower().split()

            # format:    up      → press
            #            release up
            if len(parts) == 1:
                key = parts[0]
                if key in self.current_state:
                    # Press
                    if not self.current_state[key]:
                        self.press_time[key] = current_time
                        self.hold_triggered[key] = False
                    self.current_state[key] = True

            elif len(parts) == 2 and parts[0] == "release":
                key = parts[1]
                if key in self.current_state:
                    self.current_state[key] = False

        # HOLD detect
        for key, down in self.current_state.items():
            if down and not self.hold_triggered[key]:
                if (current_time - self.press_time[key]) > self.hold_duration:
                    self.hhold_triggered[key] = True

    # ------------------- Queries -------------------

    def is_pressed(self, button):
        return self.current_state[button]

    def just_pressed(self, button):
        return self.current_state[button] and not self.previous_state[button]

    def just_released(self, button):
        return not self.current_state[button] and self.previous_state[button]

    def is_click(self, button):
        return self.just_released(button) and not self.prev_hold_triggered[button]

    def just_held(self, button):
        return self.hold_triggered[button] and not self.prev_hold_triggered[button]

    def is_repeating(self, button):
        if not self.current_state[button]:
            return False

        held_time = time.time() - self.press_time[button]
        if held_time < self.repeat_delay:
            return False

        t = held_time - self.repeat_delay

        # trigger repeat once each repeat_rate
        return int(t / self.repeat_rate) > int((t - 0.016) / self.repeat_rate)
