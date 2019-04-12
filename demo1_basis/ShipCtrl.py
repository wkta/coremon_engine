from cgm_engine import *


class ShipCtrl(EventReceiver):

    def __init__(self, ref_mod, rocksm):
        super().__init__()
        self._ref_ship = ref_mod
        self._ref_rocks = rocksm
        self.last_tick = None

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            ba = pygame.key.get_pressed()
            if ba[PygameBridge.K_UP]:
                self._ref_ship.accel()
            if ba[PygameBridge.K_DOWN]:
                self._ref_ship.brake()
            if ba[PygameBridge.K_RIGHT]:
                self._ref_ship.cw_rotate()
            if ba[PygameBridge.K_LEFT]:
                self._ref_ship.ccw_rotate()

            if self.last_tick:
                tmp = ev.curr_t - self.last_tick
            else:
                tmp = 0
            self.last_tick = ev.curr_t

            self._ref_ship.update(tmp)
            self._ref_rocks.update(tmp)

        elif ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_TAB:
                self._ref_ship.dash()
