import pygame
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver
from defs4 import GameStates


class MenuScreenCtrl(EventReceiver):
    
    def __init__(self):
        super().__init__()

    #override
    def proc_event(self,ev,source=None):
        if ev.type==PygameBridge.MOUSEBUTTONUP:
            print('pushing the ClickChallg state onto the stack...')
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.ClickChallg)
