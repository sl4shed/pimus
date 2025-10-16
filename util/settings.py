import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from ui.hmenu import hmenu
from lib.bluetooth import Bluetooth
from ui.vmenu import vmenu


class Settings:
    def __init__(
        self,
        config: Config,
        screen: Screen,
        controller: Controller,
        bluetooth: Bluetooth,
    ):
        self.config: Config = config
        self.screen: Screen = screen
        self.controller: Controller = controller
        self.bt: Bluetooth = bluetooth

        self.menu = hmenu("Options", self.screen, self.controller, self.config)

        self.menu.add_entry("Bluetooth", {"callback": self.bluetooth})
        self.menu.add_entry("Wi-Fi", {"callback": self.wifi})
        self.menu.add_entry("Display", {"callback": self.display})

    def bluetooth(self):
        # todo progress bar here
        self.bt.start_discovery()
        time = int(self.config.get("bluetooth_discovery_time"))
        pygame.time.wait(time)
        self.bt.stop_discovery()
        self.menu = vmenu("Bluetooth", self.screen, self.controller, self.config)

        self.devices = self.bt.get_devices()
        self.bt_connected = False
        for device in self.devices:
            if not device["Connected"]:
                self.menu.add_entry(
                    device["Name"],
                    {"callback": self.bt_connect, "argument": device["Address"]},
                )
            else:
                self.bt_connected = True
        if self.bt_connected:
            self.menu.add_entry(
                "Disconnect All", {"centered": True, "callback": self.bt_disconnect_all}
            )

    def bt_disconnect_all(self):
        for device in self.devices:
            if device["Connected"]:
                self.bt.disconnect(device["Address"])

    def bt_connect(self, address):
        device = None
        for device in self.devices:
            if device["Address"] == address:
                device = device
                break
        if device:
            self.bt.connect(device["Address"])

    def bt_disconnect(self, address):
        pass

    def wifi(self):
        pass

    def display(self):
        pass

    def update(self):
        self.menu.update()
