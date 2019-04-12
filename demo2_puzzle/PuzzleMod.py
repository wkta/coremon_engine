import random


class Carre:
    def __init__(self, color_order):
        assert(len(color_order) == 4)
        self._color_order = list(color_order)

    @classmethod
    def gen_random(cls):
        tmp = list(range(4))
        random.shuffle(tmp)
        return cls(tmp)

    def get_order(self):
        return self._color_order

    def rotate(self):
        self._color_order.reverse()
        prems = self._color_order.pop()
        self._color_order.insert(0, prems)
        self._color_order.reverse()

    @classmethod
    def dummy_red(cls):
        return cls((2,2,2,2))

    @classmethod
    def create_compat(cls, one_square, dir):
        remaining = [0, 1, 2, 3]
        random.shuffle(remaining)

        k = (dir + 2) % 4
        caract = [None, ] * 4

        matching_code = one_square.get_order()[dir]
        caract[k] = matching_code

        remaining.remove(matching_code)

        while len(remaining) != 0:
            tmp = remaining.pop()
            if caract[0] is None:
                caract[0] = tmp
            elif caract[1] is None:
                caract[1] = tmp
            elif caract[2] is None:
                caract[2] = tmp
            elif caract[3] is None:
                caract[3] = tmp

        return cls(caract)

    @classmethod
    def create_super_compat(cls, sq1, dir1, sq2, dir2):
        remaining = [0, 1, 2, 3]
        random.shuffle(remaining)

        k1 = (dir1 + 2) % 4
        k2 = (dir2 + 2) % 4
        caract = [None, ] * 4

        matching_code = sq1.get_order()[dir1]
        caract[k1] = matching_code
        remaining.remove(matching_code)

        matching_code = sq2.get_order()[dir2]
        caract[k2] = matching_code
        remaining.remove(matching_code)

        # complétion
        while len(remaining) != 0:
            tmp = remaining.pop()
            if caract[0] is None:
                caract[0] = tmp
            elif caract[1] is None:
                caract[1] = tmp
            elif caract[2] is None:
                caract[2] = tmp
            elif caract[3] is None:
                caract[3] = tmp
        return cls(caract)


class PuzzleMod:
    NB_SQUARES = 9  # 3 x 3

    def __init__(self):
        self._grid = list()
        self.reset_state()

    def reset_state(self):
        self._grid = [None,] * 9

        solvable = False
        while not solvable:
            try:
                c_square = Carre.gen_random()
                self._grid[4] = c_square

                self._grid[5] = e_square = Carre.create_compat(c_square, 0)
                self._grid[1] = n_square = Carre.create_compat(c_square, 1)
                self._grid[3] = w_square = Carre.create_compat(c_square, 2)
                self._grid[7] = s_square = Carre.create_compat(c_square, 3)

                self._grid[0] = Carre.create_super_compat(n_square, 2, w_square, 1)
                self._grid[2] = Carre.create_super_compat(n_square, 0, e_square, 1)
                self._grid[6] = Carre.create_super_compat(w_square, 3, s_square, 2)
                self._grid[8] = Carre.create_super_compat(s_square, 0, e_square, 3)
            except ValueError:
                continue
            solvable = True

        # - we make the problem HARD
        #random.shuffle(self._grid)
        for k, sq in enumerate(self._grid):
            if k % 2 == 0:
                sq.rotate()
            elif k % 3 == 0:
                sq.rotate()
                sq.rotate()

    def get_grid(self):
        return self._grid

    def rotate(self, sq_no):
        self._grid[sq_no].rotate()

    def permute(self, sq_source, sq_dest):
        tmp = self._grid[sq_dest]
        self._grid[sq_dest] = self._grid[sq_source]
        self._grid[sq_source] = tmp
