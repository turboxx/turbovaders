import sys
import contextlib

from game.options import Options

with contextlib.redirect_stdout(None):
    import pygame

pygame.init()

import constants
from game.game import Game
from game.screens.game import ScreenGame
from game.screens.menu import ScreenMenu
from game.screens.result import ScreenResult

WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))


def initScreens(win, clock, options: Options):
    menuScreen = ScreenMenu(win, clock, options)
    gameScreen = ScreenGame(win, clock, options)
    resultScreen = ScreenResult(win, clock, options)

    return [menuScreen, gameScreen, resultScreen]


# primitive stage manager
def changeState(old_state, new_state, active_screen, screens):
    [menuScreen, gameScreen, resultScreen] = screens
    active_screen.unload()

    if new_state == constants.STATE_GAME:
        active_screen = gameScreen
    elif new_state is constants.STATE_RESULT:
        active_screen = resultScreen
    elif new_state is constants.STATE_MENU:
        active_screen = menuScreen

    return new_state, active_screen


def main():
    run = True
    state = constants.STATE_MENU
    clock = pygame.time.Clock()
    options = Options()

    # loading all screens, dirty solution todo: improve
    screens = initScreens(WIN, clock, options)

    # should be menu
    activeScreen = screens[0]
    game = Game(WIN, clock, options)

    while run:
        # how does pygame.event.get() work???
        # event binding
        for event in pygame.event.get():
            # kill program on esc
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if state == constants.STATE_MENU or state == constants.STATE_RESULT:
                    # kill program on esc when not in game
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break

                    if event.key == pygame.K_SPACE:
                        # start new game
                        game = Game(WIN, clock, options)
                        (state, activeScreen) = changeState(state, constants.STATE_GAME, activeScreen, screens)
                        continue

            # generic passing event to screens to handle
            # only ScreenGame cares so far
            activeScreen.handleEvent(event)

        if state == constants.STATE_GAME:
            game.tick()
            if game.has_ended:
                (state, activeScreen) = changeState(state, constants.STATE_RESULT, activeScreen, screens)

        # rendering
        activeScreen.setGame(game).load().render()
        pygame.display.update()

    # kill
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)


main()
