from lib.config import Config
from lib.control import Controller
from lib.lcd import Screen
from ui.progressbar import ProgressBar
from util import utils


class Player:
    def __init__(self, songs, config: Config, screen: Screen, controller: Controller):
        self.songs = songs
        self.config = config
        self.screen = screen
        self.controller = controller

        self.playing = False
        self.last_song_index = -1
        self.song_index = 0
        current_song = self.songs[self.song_index]
        self.song_start_time = utils.millis()
        self.pause_start_time = None
        self.total_pause_time = 0
        self.menu = ProgressBar(0, current_song.title, self.config, self.screen)

    def update(self):
        self.menu.update()

        # song update
        current_song = self.songs[self.song_index]

        # Calculate actual playback time, excluding paused time
        current_time = utils.millis()
        if current_song.paused and self.pause_start_time is None:
            self.pause_start_time = current_time
        elif not current_song.paused and self.pause_start_time is not None:
            self.total_pause_time += current_time - self.pause_start_time
            self.pause_start_time = None

        if current_song.paused:
            song_progress_duration = int(
                (self.pause_start_time - self.song_start_time - self.total_pause_time)
                / 1000
            )
        else:
            song_progress_duration = int(
                (current_time - self.song_start_time - self.total_pause_time) / 1000
            )
        if (
            current_song.duration < song_progress_duration
            and self.song_index + 1 <= len(self.songs)
        ):
            self.playing = False
            self.song_index += 1
        song_progress = int((100 * song_progress_duration) / current_song.duration)

        self.menu.set_progress(song_progress)
        self.menu.set_title(current_song.title)
        if not self.playing and self.last_song_index != self.song_index:
            current_song.play()
            self.last_song_index = self.song_index
            self.playing = True
            self.song_start_time = utils.millis()
            self.pause_start_time = None
            self.total_pause_time = 0

        # input handling
        if self.controller.is_click("select"):
            self.playing = current_song.cycle_pause()
        elif self.controller.is_pressed("select") and self.controller.is_click("right"):
            # skip song
            if self.song_index + 1 <= len(self.songs):
                self.playing = False
                self.song_index += 1
                self.pause_start_time = None
                self.total_pause_time = 0
        elif self.controller.is_pressed("select") and self.controller.is_click("left"):
            # skip song
            if self.song_index - 1 > 0:
                self.playing = False
                self.song_index -= 1
                self.pause_start_time = None
                self.total_pause_time = 0
        elif self.controller.is_pressed("select") and self.controller.is_click("up"):
            # volume up
            current_song.set_volume(current_song.get_volume() + 5)
        elif self.controller.is_pressed("select") and self.controller.is_click("down"):
            # volume down
            current_song.set_volume(current_song.get_volume() - 5)

    def skip(self):
        if self.song_index + 1 <= len(self.songs):
            self.playing = False
            self.last_song_index = self.song_index
            self.song_index += 1
            self.pause_start_time = None
            self.total_pause_time = 0
