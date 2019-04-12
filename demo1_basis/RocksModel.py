import random

from gameobjects.Vector2d import Vector2d
from glvars import SCREEN_SIZE
import math


class RocksModel:
    INIT_NB = 7

    def __init__(self):
        self.contents = list()
        for i in range(self.INIT_NB):
            rand_pos = [random.randint(0, SCREEN_SIZE[0]-1), random.randint(0, SCREEN_SIZE[1]-1)]
            rand_size = random.randint(8, 55)
            rand_angle = random.uniform(0, 2 * math.pi)
            rand_speed_val = random.uniform(4, 32)
            speedvect = Vector2d.new_from_angle(rand_angle)
            speedvect.multiply(rand_speed_val)

            self.contents.append(
                [rand_pos, rand_size, speedvect]
            )

    @staticmethod
    def _adjust_for_torus(coordx, coordy):
        resx, resy = coordx, coordy
        # - torus mode
        if coordx < 0:
            resx = coordx + SCREEN_SIZE[0]
        elif coordx >= SCREEN_SIZE[0]:
            resx = coordx - SCREEN_SIZE[0]

        if coordy < 0:
            resy = coordy + SCREEN_SIZE[1]
        elif coordy >= SCREEN_SIZE[1]:
            resy = coordy - SCREEN_SIZE[1]

        return resx, resy

    def update(self, time_elapsed):
        for i in range(len(self.contents)):
            speedvect = self.contents[i][2]
            self.contents[i][0][0] += time_elapsed * speedvect.x
            self.contents[i][0][1] += time_elapsed * speedvect.y
            self.contents[i][0][0], self.contents[i][0][1] = RocksModel._adjust_for_torus( self.contents[i][0][0], self.contents[i][0][1] )
