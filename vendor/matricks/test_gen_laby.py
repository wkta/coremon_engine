from tests.GameEngine import GameEngine
from tests.lsettings import BG_COLOR_CODE
import pygame
from pygame.locals import *


from tests.Afficheur import Afficheur
from tools.IntegerMatrix import IntegerMatrix
from tools.RandomMaze import RandomMaze


class Test( GameEngine) :

    def __init__(self):
        super().__init__()
        self.__newGeneration()
        self.gen_requested = False

    def __newGeneration(self):
        self.maze = RandomMaze( 33, 33, 3, 5, 480 ) #taill impaire souhaitee!!!!
        self.aff = Afficheur( self.maze.getMatrix() )

    def handleEvents(self):
        li_ev = pygame.event.get()
        for ev in li_ev:
            if ev.type==QUIT:
                self.flagExit()
            elif ev.type==MOUSEBUTTONDOWN:
                #bt = pygame.mouse.get_pressed()
                #if bt[0]:
                #   if self.maze.canMerge():
                #       self.maze.stepMerge()
                
                self.gen_requested = True

    def drawContent(self):
        self.window.fill(
            pygame.color.Color(BG_COLOR_CODE)
            )
        self.aff.draw( self.window )
        
    def update(self):
        if self.gen_requested:
            self.__newGeneration()
            self.gen_requested = False


test = Test()
while test.isRunning():
    test.handleEvents()
    test.update()
    test.draw()
del test
