# those two lines are useful if running without PyCharm /proper "Content Root" settings...
import sys
sys.path.append('../vendor')

import coremon_main
from NinjamazeCtrl import NinjamazeCtrl
from NinjamazeMod import NinjamazeMod
from NinjamazeView import NinjamazeView
from coremon_main.runners import VanillaGameCtrl
import glvars


"""
in this demo, we're gonna use cool tools:
- matricks.RandomMaze to create a proceduraly-generated level
- gameobjects.SpriteSheet to load a tileset
"""

coremon_main.init(glvars.SCR_SIZE, glvars.MAZENINJA_CAPTION)
m = NinjamazeMod()
v = NinjamazeView(m)
c = NinjamazeCtrl(m)
ctrl = VanillaGameCtrl()

# - run the game
print('------------')
print('CONTROLS:')
print('* use arrows to move')
print('* use SPACE to generate a new level')
print('------------')
print()

v.turn_on()
c.turn_on()
ctrl.turn_on()
ctrl.loop()

coremon_main.cleanup()
print('done.')
