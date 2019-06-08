from coremon_main import CogObject
from defs3 import MyEvTypes
from matricks.RandomMaze import RandomMaze


class NinjamazeMod(CogObject):

    def __init__(self):
        super().__init__()
        # constructor:
        #    RandomMaze(w, h, min_room_size, max_room_size, density_factor=140)
        self.rm = None
        self.player_pos = None
        self.reset_level()

    def reset_level(self):
        w, h = 24, 24
        self.rm = RandomMaze(w, h, 3, 5)
        self.pev(MyEvTypes.NewLevel)

        self.player_pos = [w//2 -1, h//2 -1]
        self.pev(MyEvTypes.PlayerMoves, new_pos=self.player_pos)

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

        self.pev(MyEvTypes.PlayerMoves, new_pos=dest)
        self.player_pos = dest

    def get_av_pos(self):
        return self.player_pos
