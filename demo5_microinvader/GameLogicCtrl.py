import time
import coremon_main
from coremon_main import EventReceiver, EngineEvTypes
import pygame
from defs5 import MyEvTypes


class GameLogicCtrl(EventReceiver):

    MOVE_SIDE_PERIOD = 1.0  # s
    MOVE_DOWN_PERIOD = 3.5  # s
    RELOADING_DELAY = 0.8

    def __init__(self):
        super().__init__(self)
        self._is_reloading = False
        t = time.time()
        self._last_moveside = self._last_movedown = t
        self._reloading_starts_at = None

    def flag_reloading(self):
        self._reloading_starts_at = time.time()

    def is_reloading(self):
        return self._reloading_starts_at is not None

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:

            if self.is_reloading():
                d = ev.curr_t - self._reloading_starts_at
                if d > self.RELOADING_DELAY:
                    self._reloading_starts_at = None  # reloading process ended
                    self.pev(MyEvTypes.PlayerReloads)

            d = ev.curr_t - self._last_moveside
            if d > self.MOVE_SIDE_PERIOD:
                self._last_moveside = ev.curr_t
                self.pev(MyEvTypes.InvadersMoveSide)

            d = ev.curr_t - self._last_movedown
            if d > self.MOVE_DOWN_PERIOD:
                self._last_movedown = ev.curr_t
                self.pev(MyEvTypes.InvadersMoveDown)
