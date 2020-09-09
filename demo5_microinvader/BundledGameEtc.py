import pygame

from coremon_main import EventReceiver, EngineEvTypes
import glvars
from defs5 import MyEvTypes


class BundledGameEtc(EventReceiver):

    def __init__(self, ref_mod, ref_gl_ctrl):
        super().__init__()
        self._mod = ref_mod
        self._gl_ctrl = ref_gl_ctrl

        self.reloaded = True
        self.move_left = False

    def proc_event(self, ev, source):

        if ev.type == MyEvTypes.InvadersMoveSide:
            for inva in self._mod.invaders:
                inva.move_ip((-10 if self.move_left else 10, 0))
            self.move_left = not self.move_left
            return

        if ev.type == MyEvTypes.InvadersMoveDown:
            for inva in self._mod.invaders:
                inva.move_ip(0, 10)
            return

        if ev.type == MyEvTypes.PlayerReloads:
            self.reloaded = True
            return

        if ev.type == EngineEvTypes.LOGICUPDATE:
            for shotobj in self._mod.shots[:]:
                shotobj.move_ip((0, -4))
                if not glvars.screen.get_rect().contains(shotobj):
                    self._mod.shots.remove(shotobj)
                else:
                    hit = False
                    for inva in self._mod.invaders[:]:
                        if inva.colliderect(shotobj):
                            hit = True
                            i = self._mod.invaders.index(inva)
                            del self._mod.colors[i]
                            del self._mod.invaders[i]
                    if hit:
                        self._mod.shots.remove(shotobj)

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                glvars.player.move_ip((-4, 0))
            if pressed[pygame.K_RIGHT]:
                glvars.player.move_ip((4, 0))

            if pressed[pygame.K_SPACE]:
                if self.reloaded:
                    self._mod.shots.append(glvars.player.copy())
                    self.reloaded = False
                    # when shooting, create a timeout of RELOAD_SPEED
                    self._gl_ctrl.flag_reloading()

            glvars.player.clamp_ip(glvars.screen.get_rect())
