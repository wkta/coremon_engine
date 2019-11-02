import pygame
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver

class ClickChallgCtrl(EventReceiver):
    
    def __init__(self):
        super().__init__()

    #override
    def proc_event(self,ev,source=None):
        if ev.type==PygameBridge.KEYDOWN and ev.key==PygameBridge.K_RETURN:
            print('event sent: removing ClickChallg state from the stack...')
            self.pev(EngineEvTypes.POPSTATE)
