import sys
import termios
import tty
import time
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

        # enable raw mode
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def __del__(self):
        # restore terminal on exit
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        except:
            pass

    # ---------------- RAW INPUT READER ---------------- #

    def _get_key(self):
        """Non-blocking read of 1 key or escape sequence."""
        if select.select([sys.stdin], [], [], 0)[0]:
            ch = sys.stdin.read(1)

            # handle escape sequences for arrows
            if ch == "\x1b":  # ESC
                if select.select([sys.stdin], [], [], 0)[0]:
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[" and select.select([sys.stdin], [], [], 0)[0]:
                        ch3 = sys.stdin.read(1)
                        seq = ch + ch2 + ch3
                        if seq == "\x1b[A":
                            return "up"
                        if seq == "\x1b[B":
                            return "down"
                        if seq == "\x1b[C":
                            return "right"
                        if seq == "\x1b[D":
                            return "left"
                return None

            # normal keys
            if ch in ("w", "W"):
                return "up"
            if ch in ("s", "S"):
                return "down"
            if ch in ("a", "A"):
                return "left"
            if ch in ("d", "D"):
                return "right"

            if ch == " " or ch == "\n":
                return "select"

            return None

        return None

    # ---------------- UPDATE ---------------- #

    def update(self, events=None):
        """Drop-in compatible with pygame version: events is ignored."""
        current_time = time.time()

        self.previous_state = self.current_state.copy()
        self.prev_hold_triggered = self.hold_triggered.copy()

        key = self._get_key()
        if key is not None:
            # treat keys as press events
            if not self.current_state[key]:
                self.press_time[key] = current_time
                self.hold_triggered[key] = False
            self.current_state[key] = True

        # auto-release keys when not held
        # (console has no KEYUP event, so we emulate)
        for btn in self.current_state:
            if btn != key:
                self.current_state[btn] = False

        # HOLD DETECT
        for key, down in self.current_state.items():
            if down and not self.hold_triggered[key]:
                if (current_time - self.press_time[key]) > self.hold_duration:
                    self.hold_triggered[key] = True

    # ---------------- QUERIES ---------------- #

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
        return int(t / self.repeat_rate) > int((t - 0.016) / self.repeat_rate)
