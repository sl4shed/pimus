from logging import Logger
import pydbus


class Bluetooth:
    def __init__(self, logger: Logger):
        self.bus = pydbus.SystemBus()
        self.adapter = self.bus.get("org.bluez", "/org/bluez/hci0")
        self.mngr = self.bus.get("org.bluez", "/")
        self.logger: Logger = logger

    def get_devices(self):
        mngd_objs = self.mngr.GetManagedObjects()
        devices = []
        for path in mngd_objs:
            device_props = mngd_objs[path].get("org.bluez.Device1", {})
            if not device_props:
                continue

            addr = device_props.get("Address")
            name = device_props.get("Name")

            if addr and name:
                devices.append(device_props)

        return devices

    def get_device(self, address):
        try:
            device = self.bus.get(
                "org.bluez", f"/org/bluez/hci0/dev_{address.replace(':', '_')}"
            )
            return device
        except Exception as e:
            self.logger.error(f"Failed to get device: {e}")
            return None

    def connect(self, address):
        device = self.get_device(address)
        if device:
            device.Connect()
            self.logger.info(f"Connected to device {address}")
        else:
            self.logger.error(f"Failed to connect to device {address}")

    def disconnect(self, address):
        device = self.get_device(address)
        if device:
            device.Disconnect()
            self.logger.info(f"Disconnected from device {address}")
        else:
            self.logger.error(f"Failed to disconnect from device {address}")

    def start_discovery(self):
        try:
            self.adapter.StartDiscovery()
            self.logger.info("Started Bluetooth discovery.")
        except Exception as e:
            self.logger.error(f"Failed to start discovery: {e}")

    def stop_discovery(self):
        try:
            self.adapter.StopDiscovery()
            self.logger.info("Stopped Bluetooth discovery.")
        except Exception as e:
            self.logger.error(f"Failed to stop discovery: {e}")
