import coremon_main
from coremon_main import *
from defs1 import *
import math
from gameobjects.Vector2d import Vector2d


class TinyWorldView(EventReceiver):
    RAD = 8
    BG_COLOR = (16, 4, 43)
    LINE_COLOR = (119, 255, 0)

    def __init__(self, ref_mod, rocksm):
        super().__init__()
        self.screen = coremon_main.screen

        self.curr_pos = ref_mod.get_scr_pos()
        self.curr_angle = ref_mod.get_orientation()

        self.ref_rocksm = rocksm

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self.screen.fill(self.BG_COLOR)
            self._draw_player(self.screen)
            self._draw_rocks(self.screen)

        elif ev.type == MyEvTypes.PlayerChanges:
            self.curr_angle = ev.angle
            self.curr_pos = ( int(ev.new_pos.x), int(ev.new_pos.y))

    def _draw_rocks(self, screen):
        for rockinfo in self.ref_rocksm.contents:
            pos = (int(rockinfo[0][0]), int(rockinfo[0][1]))
            size = rockinfo[1]
            pygame.draw.circle(screen, self.LINE_COLOR, pos, size, 3)

    def _draw_player(self, surface):
        orientation = -self.curr_angle
        pt_central = self.curr_pos

        temp0 = Vector2d.new_from_angle(orientation - (2.0 * math.pi / 3))
        temp0.y *= -1
        temp0.multiply(1.2 * self.RAD)

        temp1 = Vector2d.new_from_angle(orientation)
        temp1.y *= -1
        temp1.multiply(3 * self.RAD)

        temp2 = Vector2d.new_from_angle(orientation + (2.0 * math.pi / 3))
        temp2.y *= -1
        temp2.multiply(1.2 * self.RAD)

        pt_li = [
            Vector2d(*pt_central),
            Vector2d(*pt_central),
            Vector2d(*pt_central)]

        pt_li[0] += temp0  # droite
        pt_li[1] += temp1  # tete
        pt_li[2] += temp2  # gauche

        for pt in pt_li:
            pt.x = round(pt.x)
            pt.y = round(pt.y)

        pygame.draw.polygon(
            surface,
            self.LINE_COLOR,
            [(pt_li[0].x, pt_li[0].y),
             (pt_li[1].x, pt_li[1].y),
             (pt_li[2].x, pt_li[2].y)],
            3
        )
