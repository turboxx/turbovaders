from file_utils import check_dev_mode


class SoundOptions:
    def __init__(self, dev_mode):
        self.canPlayMusic = False if dev_mode else True
        # 100 is currently too fucking loud from the get go
        self.volumeMusic = 30
        self.volumeSFX = 100

    def toggleMute(self):
        self.canPlayMusic = not self.canPlayMusic

    def getVolumeMusic(self):
        return 0 if not self.canPlayMusic else self.volumeMusic

    def setVolumeMusic(self, volume: int):
        self.volumeMusic = volume

    def setVolumeSFX(self, volume: int):
        self.volumeMusic = volume


class Options:
    def __init__(self):
        self.load()
        self.devMode = check_dev_mode()
        self.sound = SoundOptions(self.devMode)

    # todo: load from some persistence
    def load(self):
        pass
