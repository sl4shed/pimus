from gpiozero import Button
import time


class Controller:
    def __init__(self, config):
        self.config = config
        self.pin_config = self.config.get("controller.pin_config")
        self.buttons = {
            button: Button(pin, bounce_time=0.02)
            for button, pin in self.pin_config.items()
        }

        self.current_state = {button: False for button in self.pin_config}
        self.previous_state = {button: False for button in self.pin_config}
        self.press_time = {button: float(0) for button in self.pin_config}
        self.repeat_delay = self.config.get("controller.repeat_delay")
        self.repeat_rate = self.config.get("controller.repeat_rate")
        self.hold_duration = self.config.get("controller.hold_duration")
        self.hold_triggered = {button: False for button in self.pin_config}
        self.prev_hold_triggered = {button: False for button in self.pin_config}

    def update(self):
        current_time = time.time()
        self.previous_state = self.current_state.copy()
        self.prev_hold_triggered = self.hold_triggered.copy()

        for button, btn_obj in self.buttons.items():
            pin_state = btn_obj.is_pressed

            if pin_state and not self.current_state[button]:
                self.press_time[button] = current_time
                self.hold_triggered[button] = False

            self.current_state[button] = pin_state

        for button, is_pressed in self.current_state.items():
            if is_pressed and not self.hold_triggered[button]:
                if (current_time - self.press_time[button]) > self.hold_duration:
                    self.hold_triggered[button] = True

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

        time_since_initial = held_time - self.repeat_delay
        return int(time_since_initial / self.repeat_rate) > int(
            (time_since_initial - 0.016) / self.repeat_rate
        )

    def cleanup(self):
        for btn in self.buttons.values():
            btn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
