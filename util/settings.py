import pygame
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from ui.hmenu import hmenu
from lib.bluetooth import Bluetooth
from ui.vmenu import vmenu
from util.timer_progressbar import TimerProgressBar


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
        # for future me navigating this mess
        # timerprogressbar has a callback where i stop bt discovery
        # matter of fact its right beneath this function
        # you dumbass
        self.menu = TimerProgressBar(
            self.config.get("bluetooth_discovery_time"),
            "Discovering Bluetooth Devices...",
            15,
            self.stop_bt_discovery,
            self.config,
            self.screen,
        )
        self.bt.start_discovery()

    def stop_bt_discovery(self):
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
        device = None
        for device in self.devices:
            if device["Address"] == address:
                device = device
                break
        if device:
            self.bt.disconnect(device["Address"])

    def wifi(self):
        pass

    def display(self):
        pass

    def update(self):
        self.menu.update()
