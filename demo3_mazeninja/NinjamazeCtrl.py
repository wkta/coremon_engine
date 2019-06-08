from coremon_main import EventReceiver, PygameBridge


class NinjamazeCtrl(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__()
        self.mod = ref_mod

    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_RIGHT:
                self.mod.push_player(0)
            elif ev.key == PygameBridge.K_UP:
                self.mod.push_player(1)
            elif ev.key == PygameBridge.K_LEFT:
                self.mod.push_player(2)
            elif ev.key == PygameBridge.K_DOWN:
                self.mod.push_player(3)
            elif ev.key == PygameBridge.K_SPACE:
                self.mod.reset_level()
