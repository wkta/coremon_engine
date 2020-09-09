import pygame

import glvars
from coremon_main import EventReceiver, EngineEvTypes


class InvadersView(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__()
        self._mod = ref_mod

    def proc_event(self, ev, source):

        if ev.type == EngineEvTypes.PAINT:
            glvars.screen.fill((0, 0, 0))

            for inva, (a, b) in zip(self._mod.invaders, self._mod.colors):
                pygame.draw.rect(glvars.screen, (150, a, b), inva)

            for shotobj in self._mod.shots:
                pygame.draw.rect(glvars.screen, (255, 180, 0), shotobj)

            pygame.draw.rect(glvars.screen, (180, 180, 180), glvars.player)
            pygame.display.flip()
