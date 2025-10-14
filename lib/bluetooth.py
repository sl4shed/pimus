import pydbus


class Bluetooth:
    def __init__(self):
        self.bus = pydbus.SystemBus()
        self.adapter = self.bus.get("org.bluez", "/org/bluez/hci0")
        self.mngr = self.bus.get("org.bluez", "/")

    def get_connected_devices(self):
        mngd_objs = self.mngr.GetManagedObjects()
        for path in mngd_objs:
            device_props = mngd_objs[path].get("org.bluez.Device1", {})
            if not device_props:
                continue

            con_state = device_props.get("Connected", False)
            addr = device_props.get("Address")
            name = device_props.get("Name")

            # Only show devices that have valid address and name, and are connected
            if con_state and addr and name:
                print(f"Device {name} [{addr}] is connected")

    def get_available_devices(self):
        mngd_objs = self.mngr.GetManagedObjects()
        for path in mngd_objs:
            device_props = mngd_objs[path].get("org.bluez.Device1", {})
            if not device_props:
                continue

            con_state = device_props.get("Connected", False)
            addr = device_props.get("Address")
            name = device_props.get("Name")

            # Only show devices that have valid address and name, and are not connected
            if not con_state and addr and name:
                print(f"Device {name} [{addr}] is available")

    def debug_all_objects(self):
        """Show all BlueZ managed objects for debugging"""
        mngd_objs = self.mngr.GetManagedObjects()
        print("\n=== All BlueZ Managed Objects ===")
        for path, interfaces in mngd_objs.items():
            print(f"\nPath: {path}")
            for interface, props in interfaces.items():
                print(f"  Interface: {interface}")
                if interface == "org.bluez.Device1":
                    print(f"    Address: {props.get('Address', 'None')}")
                    print(f"    Name: {props.get('Name', 'None')}")
                    print(f"    Alias: {props.get('Alias', 'None')}")
                    print(f"    Connected: {props.get('Connected', False)}")
                    print(f"    Paired: {props.get('Paired', False)}")
                    print(f"    Trusted: {props.get('Trusted', False)}")

    def get_all_devices(self):
        """Show all devices, even those without names"""
        mngd_objs = self.mngr.GetManagedObjects()
        print("\n=== All Bluetooth Devices ===")
        for path in mngd_objs:
            device_props = mngd_objs[path].get("org.bluez.Device1", {})
            if not device_props:
                continue

            con_state = device_props.get("Connected", False)
            addr = device_props.get("Address", "Unknown")
            name = device_props.get("Name", "No Name")
            alias = device_props.get("Alias", "No Alias")
            paired = device_props.get("Paired", False)

            status = "Connected" if con_state else "Available"
            pair_status = "Paired" if paired else "Not Paired"

            print(f"Device: {name} / {alias} [{addr}] - {status}, {pair_status}")

    def start_discovery(self):
        """Start scanning for nearby Bluetooth devices"""
        try:
            self.adapter.StartDiscovery()
            print("Started Bluetooth discovery...")
        except Exception as e:
            print(f"Failed to start discovery: {e}")

    def stop_discovery(self):
        """Stop scanning for Bluetooth devices"""
        try:
            self.adapter.StopDiscovery()
            print("Stopped Bluetooth discovery")
        except Exception as e:
            print(f"Failed to stop discovery: {e}")

    def scan_and_show_devices(self, duration=10):
        """Scan for devices and show results"""
        import time

        print(f"Scanning for Bluetooth devices for {duration} seconds...")
        self.start_discovery()
        time.sleep(duration)
        self.stop_discovery()
        print("\nDevices found:")
        self.get_all_devices()
