from termcolor import cprint

from util.broadcast import Broadcast


class Logger:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "a+")

    def info(self, message):
        cprint(f"[Info] {message}", "blue")
        self.file.write(f"\n[Info] {message}")

    def warn(self, message):
        cprint(f"[Warn] {message}", "yellow")
        self.file.write(f"\n[Warn] {message}")

    def error(self, message):
        cprint(f"[Error] {message}", "red")
        self.file.write(f"\n[Error] {message}")

    def close(self):
        self.file.close()

    def broadcast(self, message):
        cprint(f"[Broadcast] {message}", "green")
        self.file.write(f"\n[Broadcast] {message}")

    def broadcast(self, message):
        cprint(f"[Broadcast] {message}", "green")
        self.file.write(f"\n[Broadcast] {message}")
        Services.menu_manager.add(Broadcast(message, 5))
