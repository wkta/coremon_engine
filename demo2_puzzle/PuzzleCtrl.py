from coremon_main import EventReceiver, PygameBridge


class PuzzleCtrl(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__()
        self._ref_mod = ref_mod

    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_RETURN:
                self._ref_mod.reset_state()
