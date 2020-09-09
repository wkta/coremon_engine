"""
author: Thomas Iwaszko
Copyright notice: this example is a re-interpretation of the program written by 'Sloth'
that can be found here:
https://stackoverflow.com/questions/24475718/pygame-custom-event
"""


# those two lines are useful if running without PyCharm /proper "Content Root" settings...
import sys
sys.path.append('../vendor')

import glvars
from BundledGameEtc import BundledGameEtc
from GameLogicCtrl import GameLogicCtrl
from InvadersView import InvadersView
from coremon_main import EventReceiver, EngineEvTypes
from coremon_main.runners import VanillaGameCtrl
from defs5 import MyEvTypes
from GameMod import GameMod
import pygame


# ----- init. jeu & init. var. globales
glvars.screen = pygame.display.set_mode(glvars.SCR_SIZE)
pygame.display.set_caption("Micro Invader")
glvars.player = pygame.Rect(150, 180, 10, 7)


# ----- composants prog
mod = GameMod()

view = InvadersView(mod)
glctrl = GameLogicCtrl()
b = BundledGameEtc(mod, glctrl)

gctrl = VanillaGameCtrl()

# activations
view.turn_on()
glctrl.turn_on()
b.turn_on()
gctrl.turn_on()

# boucle de jeu
gctrl.loop()

print('GAME OVER.')
pygame.quit()
