import constants
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText

MUSIC_FILE = 'assets/sfx/music_menu.wav'


class ScreenResult(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, MUSIC_FILE)

    def render(self):
        self.win.fill(constants.WHITE)

        if not self.game:
            return

        statusText = 'You have lost' if self.game.hasLost else 'Victory'
        middleText = '' if self.game.hasLost else f'Score: {self.game.score}'
        startGameText = 'Press Space To Start'

        renderText(self.win, statusText, constants.BLACK, 36, (constants.WIDTH / 2, constants.HEIGHT / 2 - 40))
        renderText(self.win, middleText, constants.BLACK, 36, (constants.WIDTH / 2, constants.HEIGHT / 2))
        renderText(self.win, startGameText, constants.BLACK, 36, (constants.WIDTH / 2, constants.HEIGHT / 2 + 40))

