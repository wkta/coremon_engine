# those two lines are useful if running without PyCharm /proper "Content Root" settings...
import sys
sys.path.append('../vendor')


import random

import coremon_main
from coremon_main import EventReceiver, EngineEvTypes
from coremon_main.runners import HeadlessRunnerCtrl
from defs6 import MyEvTypes


class RandomTickerCtrl(EventReceiver):

    def __init__(self):
        super().__init__()
        self._last_checkdate = None
        self._delaybeforetick = 0.1  # sec
        self.n = 1

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:

            if self._last_checkdate is None:
                self._last_checkdate = ev.curr_t
                return

            elapsed = ev.curr_t - self._last_checkdate
            if elapsed > self._delaybeforetick:
                self._delaybeforetick = random.uniform(0.17, 4.6789)
                self._last_checkdate = ev.curr_t
                self.pev(MyEvTypes.TickOccured, rank=self.n, nexttick_in=self._delaybeforetick)
                self.n += 1


class TickPrinter(EventReceiver):

    def proc_event(self, ev, source):
        if ev.type == MyEvTypes.TickOccured:
            print('TickerPrinter is receiving tick #{}. Next tick in: {:.2f}sec'.format(ev.rank, ev.nexttick_in))


# - main program
coremon_main.init_headless()

# still using the mvc pattern
v = TickPrinter()
random_ticker = RandomTickerCtrl()
prog_ctrl = HeadlessRunnerCtrl(0.15)  # updates every 0.15sec

# activating engine components
v.turn_on()
random_ticker.turn_on()
prog_ctrl.turn_on()

# game loop, then exit
try:
    prog_ctrl.loop()
except KeyboardInterrupt:
    print('user pressed ctrl+C, exiting...')
    coremon_main.cleanup()
