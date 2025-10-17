from lib.config import Config
from lib.lcd import Screen
from ui.progressbar import ProgressBar
from util import utils


class TimerProgressBar:
    def __init__(self, time, title, size, callback, config: Config, screen: Screen):
        self.progress = 0
        self.title = title
        self.time = time
        self.start_time = utils.millis()
        self.size = size
        self.config = config
        self.screen = screen
        self.callback = callback
        self.menu = ProgressBar(
            self.progress, self.title, self.config, self.screen, self.size
        )

    def update(self):
        time_passed = utils.millis() - self.start_time
        progress = (time_passed * 100) / self.time

        if progress >= 100:
            self.callback()
            return

        self.menu.set_progress(progress)
        self.menu.update()
