from lib.bluetooth import Bluetooth
from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from lib.services import Services
from ui.hmenu import hmenu
from ui.timer_progressbar import TimerProgressBar
from ui.vmenu import vmenu


class Settings:
    def __init__(self):
        self.config: Config = Services.config
        self.screen: Screen = Services.screen
        self.controller: Controller = Services.controller
        self.bt: Bluetooth = Services.bluetooth

        self.menu = hmenu("Options")

        self.menu.add_entry("Bluetooth", {"callback": self.bluetooth})
        self.menu.add_entry("Wi-Fi", {"callback": self.wifi})
        self.menu.add_entry("Display", {"callback": self.display})

        self.screen.clear()
        self.menu.draw()

    def bluetooth(self):
        # for future me navigating this mess
        # timerprogressbar has a callback where i stop bt discovery
        # matter of fact its right beneath this function
        self.bt.start_discovery()
        Services.app.menu_manager.add(
            TimerProgressBar(
                self.config.get("bluetooth_discovery_time"),
                "Discovering Bluetooth Devices...",
                15,
                self.stop_bt_discovery,
            ),
            {"backable": False},  # forces you to wait 10 seconds lmao
        )

    def stop_bt_discovery(self):
        self.bt.stop_discovery()
        Services.app.menu_manager.back(True)  # force ts to go bakc
        # todo:::::: make the bluetooth a separate menu along with the timer in a separate class from settings :)
        self.menu = vmenu("Bluetooth")

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

    def draw(self):
        self.menu.draw()
