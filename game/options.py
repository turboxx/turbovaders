from constants import Color
from file_utils import check_dev_mode


class SoundOptions:
    def __init__(self, dev_mode):
        self.can_play_music = False if dev_mode else True
        # 100 is currently too fucking loud from the get go
        self.volume_music = 30
        self.volume_sfx = 100

    def toggle_mute(self):
        self.can_play_music = not self.can_play_music

    def get_volume_music(self):
        return 0 if not self.can_play_music else self.volume_music

    def set_volume_music(self, volume: int):
        self.volume_music = volume

    def set_volume_sfx(self, volume: int):
        self.volume_music = volume


class UIOptions:
    def __init__(self, dev_mode: bool):
        self.dark_mode = False

    def get_primary_text_color(self):
        return Color.BLACK if not self.dark_mode else Color.WHITE

    def get_primary_bg_color(self):
        return Color.WHITE if not self.dark_mode else Color.BLACK

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode


class Options:
    def __init__(self):
        self.load()
        self.dev_mode = check_dev_mode()
        self.sound = SoundOptions(self.dev_mode)
        self.ui = UIOptions(self.dev_mode)

    # todo: load from some persistence
    def load(self):
        pass
