from coremon_main import CogObject
from defs3 import MyEvTypes
from matricks.BoolMatrix import BoolMatrix
from matricks.RandomMaze import RandomMaze
from matricks.rpas import FOVCalc


class NinjamazeMod(CogObject):

    VISION_RANGE = 4  # cells
    fov_computer = None

    def __init__(self):
        super().__init__()
        self.rm = None
        self.player_pos = None
        self.visibility_m = None
        self.reset_level()

    def _update_vision(self, i, j):
        if self.fov_computer is None:
            self.fov_computer = FOVCalc()

        self.visibility_m.set_val(i, j, True)

        def func_visibility(a, b):
            if self.visibility_m.is_out(a, b):
                return False
            if self.rm.getMatrix().get_val(a, b) is None:  # cannot see through walls
                return False
            return True
        li_visible = self.fov_computer.calc_visible_cells_from(i, j, self.VISION_RANGE, func_visibility)

        for c in li_visible:
            self.visibility_m.set_val(c[0], c[1], True)

    def reset_level(self):
        w, h = 24, 24
        self.rm = RandomMaze(w, h, min_room_size=3, max_room_size=5)
        self.visibility_m = BoolMatrix((w,h))
        self.visibility_m.setAllValues(False)  # hiding all cells

        # getting a valid initial position for the avatar
        self.player_pos = self.rm.pick_walkable_cell()

        # now, the avatar can see.
        self._update_vision(*self.player_pos)

        self.pev(MyEvTypes.NewLevel)
        self.pev(MyEvTypes.PlayerMoves, new_pos=self.player_pos)

    def can_see(self, cell):
        return self.visibility_m.get_val(*cell)

    def get_terrain(self):
        return self.rm.getMatrix()

    def push_player(self, dir):
        deltas = {
            0: (+1,  0),
            1: ( 0, -1),
            2: (-1,  0),
            3: ( 0, +1)
        }
        delta = deltas[dir]
        dest = list(self.player_pos)
        dest[0] += delta[0]
        dest[1] += delta[1]
        t = self.get_terrain()
        if t.is_out(*dest):  # out of bounds
            return
        if t.get_val(*dest) is None:  # wall
            return

        self.player_pos = dest
        self._update_vision(*dest)
        self.pev(MyEvTypes.PlayerMoves, new_pos=dest)

    def get_av_pos(self):
        return self.player_pos
