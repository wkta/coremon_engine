# those two lines are useful if running without PyCharm /proper "Content Root" settings...
import sys
sys.path.append('../vendor')

import coremon_main
from coremon_main.runners import StackBasedGameCtrl
from defs4 import GameStates
from glvars import SCR_SIZE, WIN_CAPTION


# - main program
coremon_main.init(
    SCR_SIZE,
    WIN_CAPTION
)
ctrl = StackBasedGameCtrl(GameStates, GameStates.MenuScreen)

# - run the game
ctrl.turn_on()
ctrl.loop()

coremon_main.cleanup()
print('done.')
