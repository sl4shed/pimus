from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from ui.hmenu import hmenu
from lib.bluetooth import Bluetooth


class Settings:
    def __init__(
        self,
        config: Config,
        screen: Screen,
        controller: Controller,
        bluetooth: Bluetooth,
    ):
        self.config = config
        self.screen = screen
        self.controller = controller
        self.bluetooth = bluetooth

        self.menu = hmenu("Options", self.screen, self.controller, self.config)

        self.menu.add_entry("Bluetooth", {"callback": self.bluetooth})
        self.menu.add_entry("Wi-Fi", {"callback": self.wifi})
        self.menu.add_entry("Display", {"callback": self.display})

    def bluetooth(self):
        self.bluetooth.scan_and_show_devices(10)

    def wifi(self):
        pass

    def display(self):
        pass

    def update(self):
        self.menu.update()
