import pygame

import coremon_main
from PuzzleMod import PuzzleMod
from coremon_main import EventReceiver, EngineEvTypes, PygameBridge
import math


class PuzzleView(EventReceiver):
    BG_COLOR = (16, 4, 43)
    SQ_COLORS = (
        (245, 125, 43),
        (0, 165, 193),
        (189, 2, 32),  # red
        (173, 200, 65)  # green
    )

    BASE_POS = (50, 50)
    OFFSET = 182

    SQ_SIZE = 180

    tested = False

    @classmethod
    def calc_pos(cls, sq_index):
        nb_col = int(math.sqrt(PuzzleMod.NB_SQUARES))
        line = sq_index // nb_col
        col = sq_index % nb_col
        return cls.BASE_POS[0] + col * cls.OFFSET, cls.BASE_POS[1] + line * cls.OFFSET

    def __init__(self, ref_mod):
        super().__init__()
        self._ref_mod = ref_mod
        self.screen = coremon_main.screen
        self.dragged_sq = None

    @classmethod
    def collision(cls, mousepos, square_no):
        # return True/False
        pt_ref = cls.calc_pos(square_no)
        if pt_ref[0] < mousepos[0] < pt_ref[0] + cls.SQ_SIZE:
            if pt_ref[1] < mousepos[1] < pt_ref[1] + cls.SQ_SIZE:
                return True
        return False

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self.screen.fill(self.BG_COLOR)
            self._draw_squares()

            # if not self.tested:

            crop_box = (560, 560)
            crop_surf = pygame.Surface(crop_box, flags=pygame.SRCALPHA)
            rect = [45, 45]
            rect.extend(crop_box)
            crop_surf.blit(self.screen, (0, 0), rect)
            dest_size = (crop_surf.get_size()[0]//2, crop_surf.get_size()[1]//2)
            img_transfo = pygame.transform.scale(crop_surf, dest_size)
            img_transfo = pygame.transform.rotate(img_transfo, 45)
            #pygame.image.save(img_transfo, 'test-blit.png')
            self.screen.blit(img_transfo, (625, 368))

        elif ev.type == PygameBridge.MOUSEBUTTONDOWN:
            mousepos = ev.pos
            for k in range(PuzzleMod.NB_SQUARES):
                if not self.collision(mousepos, k):
                    continue

                #if ev.button == 3:
                self._ref_mod.rotate(k)

                # - if you can move squares, it becomes REALLY hard, we better don't do it
                # --
                # elif ev.button == 1:
                #     self.dragged_sq = k
                #     print('tire {}'.format(k))

        # elif ev.type == PygameBridge.MOUSEBUTTONUP:
        #     if self.dragged_sq is not None:
        #         mousepos = ev.pos
        #
        #         dest = -1
        #         for k in range(PuzzleMod.NB_SQUARES):
        #             if self.collision(mousepos, k):
        #                 dest = k
        #                 break
        #
        #         if dest != -1:  # permute two squares
        #             self._ref_mod.permute(self.dragged_sq, dest)
        #         self.dragged_sq = None

    def _draw_squares(self):
        rect4 = list()
        for k, sq in enumerate(self._ref_mod.get_grid()):
            del rect4[:]
            rect4.extend(self.calc_pos(k))
            rect4.append(self.SQ_SIZE)
            rect4.append(self.SQ_SIZE)

            pygame.draw.rect(self.screen, (50,50,50), rect4, 2)
            tmp = sq.get_order()
            for num_tri in range(4):
                tmppos = self.calc_pos(k)

                pt_a = tmppos
                pt_b = (tmppos[0] + self.SQ_SIZE//2, tmppos[1] + self.SQ_SIZE//2)
                pt_c = (tmppos[0] + self.SQ_SIZE, tmppos[1])

                if num_tri == 2:
                    pt_c = (tmppos[0], tmppos[1] + self.SQ_SIZE)
                elif num_tri == 3:
                    pt_a = (tmppos[0] , tmppos[1] + self.SQ_SIZE)
                    pt_c = (tmppos[0]+self.SQ_SIZE, tmppos[1] + self.SQ_SIZE)
                elif num_tri == 0:
                    pt_a = (tmppos[0] + self.SQ_SIZE, tmppos[1])
                    pt_c = (tmppos[0] + self.SQ_SIZE, tmppos[1] + self.SQ_SIZE)

                color_code = tmp[num_tri]
                adhoc_color = self.SQ_COLORS[color_code]

                pygame.draw.polygon(self.screen, adhoc_color, (pt_a, pt_b, pt_c))
