import coremon_main
from coremon_main import EventReceiver, EngineEvTypes
import pygame

from defs3 import MyEvTypes
from gameobjects.SpriteSheet import SpriteSheet
import os


class NinjamazeView(EventReceiver):

    CELL_SIDE = 32  # px
    WALL_COLOR = (8, 8, 24)
    HIDDEN_CELL_COLOR = (24, 24, 24)

    def __init__(self, ref_mod):
        super().__init__()
        self.assoc_r_col = dict()
        grid_rez = (16, 16)

        img = pygame.image.load(os.path.join('assets', 'tileset.png')).convert()
        self.tileset = SpriteSheet(img, grid_rez)
        img = pygame.image.load(os.path.join('assets', '1.png')).convert()
        self.planche_avatar = SpriteSheet(
            img,
            grid_rez,
            colorkey=(255,0,255)
        )
        self.mod = ref_mod
        self.avatar_apparence = self.planche_avatar.getSpriteNo(0)
        self.pos_avatar = ref_mod.get_av_pos()

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self._draw_content(coremon_main.screen)
        elif ev.type == MyEvTypes.PlayerMoves:
            self.pos_avatar = ev.new_pos

    def _draw_content(self, scr):
        scr.fill(self.WALL_COLOR)

        nw_corner = (0, 0)
        tmp_r4 = [None, None, None, None]

        tuile = self.tileset.getSpriteNo(912)

        dim = self.mod.get_terrain().get_size()
        for i in range(dim[0]):
            for j in range(dim[1]):
                # ignoring walls
                tmp = self.mod.get_terrain().get_val(i, j)
                if tmp is None:
                    continue

                tmp_r4[0], tmp_r4[1] = nw_corner
                tmp_r4[0] += i * self.CELL_SIDE
                tmp_r4[1] += j * self.CELL_SIDE
                tmp_r4[2] = tmp_r4[3] = self.CELL_SIDE
                if not self.mod.can_see((i,j)):  # hidden cell
                    pygame.draw.rect(scr, self.HIDDEN_CELL_COLOR, tmp_r4)
                else:  # visible tile
                    scr.blit(tuile, tmp_r4)

        # draw avatar process
        av_i, av_j = self.pos_avatar[0] * self.CELL_SIDE, self.pos_avatar[1] * self.CELL_SIDE
        scr.blit(self.avatar_apparence, (av_i, av_j, 32, 32) )
