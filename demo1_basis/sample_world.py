
# Python bytecode 3.1 (3151)
# Embedded file name: C:\Users\Thomas\Desktop\coremonger\demo1_simpleworld\sample_world.py
# Compiled at: 2019-03-07 17:09:22
import cgm_engine
from cgm_engine import *
from cgm_engine._events import CogObject
from defs1 import *

class AvatarMod(CogObject):
    DASH_SIZE = 45

    def __init__(self):
        super().__init__(explicit_id=1)
        self.pos_avatar = [0, 0]

    def get_pos(self):
        return self.pos_avatar

    def _broadcast_new_pos(self):
        self.pev(MyEvTypes.PlayerMoves, new_pos=self.pos_avatar)

    def move_avatar(self, new_pos):
        self.pos_avatar[0], self.pos_avatar[1] = new_pos
        self._broadcast_new_pos()

    def increm_x(self):
        self.pos_avatar[0] += 1
        self._broadcast_new_pos()

    def y_dash(self):
        self.pos_avatar[1] += self.DASH_SIZE
        self._broadcast_new_pos()


class SampleView(EventReceiver):
    RAD = 8

    def __init__(self, ref_mod):
        super().__init__()
        self.ref_mod = ref_mod
        self.av_drawn_at = list(self.ref_mod.get_pos())
        self.av_color = pygame.Color('orange')
        self.screen = cgm_engine.screen

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self.screen.fill((250, 33, 33))
            pygame.draw.circle(self.screen, self.av_color, self.av_drawn_at, self.RAD)
        else:
            if ev.type == PygameBridge.MOUSEBUTTONDOWN:
                print(('clic bt= {} / pos= {}').format(ev.button, ev.pos))
                self.ref_mod.move_avatar(ev.pos)
            else:
                if ev.type == MyEvTypes.PlayerMoves:
                    self.av_drawn_at[0], self.av_drawn_at[1] = ev.new_pos


class AvatarCtrl(EventReceiver):
    DELTA = 0.04

    def __init__(self, ref_mod):
        super().__init__()
        self.ref_mod = ref_mod
        self.last_mvt = None
        return

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            tmp = ev.curr_t
            if self.last_mvt is None or tmp - self.last_mvt > self.DELTA:
                self.ref_mod.increm_x()
                self.last_mvt = tmp
        else:
            if ev.type == PygameBridge.KEYDOWN and ev.key == PygameBridge.K_TAB:
                self.ref_mod.y_dash()
            return
