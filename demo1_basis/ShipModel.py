from cgm_engine import *
from defs1 import *
from gameobjects.Vector2d import Vector2d
from glvars import SCREEN_SIZE
import random


class ShipModel(CogObject):
    DASH_DISTANCE = 128
    DELTA_ANGLE = 0.04
    SPEED_CAP = 256

    def __init__(self):
        super().__init__(explicit_id=1)
        rand_pos = (random.randint(0, SCREEN_SIZE[0] - 1), random.randint(0, SCREEN_SIZE[1] - 1))
        self._position = Vector2d(*rand_pos)
        self._angle = 0
        self._speed = Vector2d()

    # - privée
    def _commit_new_pos(self):
        # - torus mode
        if self._position.x < 0:
            self._position.x += SCREEN_SIZE[0]
        elif self._position.x >= SCREEN_SIZE[0]:
            self._position.x -= SCREEN_SIZE[0]
        if self._position.y < 0:
            self._position.y += SCREEN_SIZE[1]
        elif self._position.y >= SCREEN_SIZE[1]:
            self._position.y -= SCREEN_SIZE[1]

        self.pev(MyEvTypes.PlayerChanges, new_pos=self._position, angle=self._angle)

    def _update_speed_vect(self):
        lg = self._speed.length()
        self._speed = Vector2d.new_from_angle(self._angle)
        self._speed.multiply(lg)

    def ccw_rotate(self):
        self._angle -= self.__class__.DELTA_ANGLE
        self._update_speed_vect()

    def cw_rotate(self):
        self._angle += self.__class__.DELTA_ANGLE
        self._update_speed_vect()

    def get_orientation(self):
        return self._angle

    def accel(self):
        if self._speed.length() == 0:
            self._speed = Vector2d.new_from_angle(self._angle)
            self._speed.multiply(5)
        else:
            speedv_now = self._speed.length()
            speedv_now += 1
            if speedv_now > self.SPEED_CAP:
                speedv_now = self.SPEED_CAP

            self._speed = Vector2d.new_from_angle(self._angle)
            self._speed.multiply(speedv_now)

    def brake(self):
        speedv_now = self._speed.length()
        speedv_now = speedv_now * 0.96
        if speedv_now < 5:
            self._speed = Vector2d()
            return

        self._speed = Vector2d.new_from_angle(self._angle)
        self._speed.multiply(speedv_now)

    def get_position(self):
        return self._position

    def get_scr_pos(self):
        return int(self._position.x), int(self._position.y)

    def set_position(self, new_pos):
        self._position.x, self._position.y = new_pos
        self._commit_new_pos()

    def update(self, temps_passe):
        self._position.x += temps_passe * self._speed.x
        self._position.y += temps_passe * self._speed.y

        self._commit_new_pos()

    def dash(self):
        tmp = Vector2d.new_from_angle(self._angle)
        tmp.multiply(self.DASH_DISTANCE)
        self._position += tmp
        self._commit_new_pos()
