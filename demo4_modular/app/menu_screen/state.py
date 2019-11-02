from coremon_main import BaseGameState, EventManager
from app.menu_screen.view import MenuScreenView
from app.menu_screen.ctrl import MenuScreenCtrl


class MenuScreenState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        print('entering MenuScreen state...')
        self.v= MenuScreenView()
        self.v.turn_on()
        self.c= MenuScreenCtrl()
        self.c.turn_on()

    def release(self):
        print('MenuScreen state is released.')
        self.c.turn_off()
        self.c= None
        self.v.turn_off()
        self.v= None

    #override
    def pause(self):
        print('MenuScreen state is paused.')
        self.c.turn_off()
        self.v.turn_off()

    #override
    def resume(self):
        print('MenuScreen state is resumed.')
        self.v.turn_on()
        self.c.turn_on()
