import random
from matricks.IntegerMatrix import IntegerMatrix


SYM_UP, SYM_DOWN, SYM_LEFT, SYM_RIGHT = range(4)

DIRS = [
    SYM_UP,
    SYM_DOWN,
    SYM_LEFT,
    SYM_RIGHT]

COORD_OFFSET = {
    SYM_UP: [0, -1],
    SYM_DOWN: [0, +1],
    SYM_LEFT: [-1, 0],
    SYM_RIGHT: [+1, 0]}


def dist_manhattan(c1, c2):
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1])


def cell_in_range(cell, size):
    if cell[0] < 0 or cell[0] >= size[0]:
        return False
    if cell[1] < 0 or cell[1] >= size[1]:
        return False
    return True


def cell_voisinnes(c, size):
    i, j = c
    res = list()
    for d in DIRS:
        voisin_direct = (i + COORD_OFFSET[d][0], j + COORD_OFFSET[d][1])
        if cell_in_range(voisin_direct, size):
            res.append(voisin_direct)
    return res


class RandomMaze:
    """
    le but de cette classe est de générer un labyrinthe aléatoire :
    représenté via une matrice 2d à valeurs abritraires (soit None soit Nombre entier)
    représentant salles et couloirs

    Elle permet de récupérer une matrice (objet type IntegerMatrix) constante et adéquate
    pour le but recherché (disposer dun labyrinthe différent à chaque fois)
    via la méthode RandomMaze.getMatrix
    """
    def __init__(self, w, h, min_room_size, max_room_size, density_factor=140):
        self.int_matrix = IntegerMatrix((w, h))
        self.room_possib_size = list()

        for i in range(min_room_size, max_room_size + 1):
            if i % 2 == 0:  # choix dune taille impaire nécessairement
                continue
            self.room_possib_size.append(i)

        # --- pr stocker meta données
        self.curr_region = 0
        self.li_rooms = list()

        # --- procédure de constr dun labyrinthe randomize

        # (1) creation non overlaping rooms
        self.nb_rooms = 0
        self.all_room_codes = set()
        NB_ESSAIS = density_factor
        for i in range(NB_ESSAIS):
            self.__add_room()

        # (2) growing tree algo
        for i in range(1, w - 1, 2):
            for j in range(1, h - 1, 2):
                pos = (i, j)
                if self.int_matrix.get_val(*pos) is None:
                    self.__growMaze(pos)

        # (3) connexion de regions (creuse les jonctions)
        self.candidats_connexion = list()
        self.li_connecteurs = list()
        dim = self.int_matrix.get_size()
        for i in range(dim[0]):
            for j in range(dim[1]):
                if self.__canBeConnector((i, j)):
                    self.candidats_connexion.append((i, j))

        self.regions_to_blobs = dict()
        while self.canMerge():
            self.stepMerge()

        # (4) suppr. cul-de-sac
        self.tested_pos = set()
        self.recUncarve((1, 1))

    def isRoomRegion(self, pos):
        val = self.int_matrix.get_val(*pos)
        return val in self.all_room_codes

    def recUncarve(self, pos):
        if pos in self.tested_pos:
            return
        self.tested_pos.add(pos)

        m_size = self.int_matrix.get_size()
        voisins = cell_voisinnes(pos, m_size)
        nb_cell_carved_v = 0  # sera un nb entre 1 et 4
        for v in voisins:
            if self.int_matrix.get_val(*v) is not None:
                nb_cell_carved_v += 1

        if nb_cell_carved_v == 1:
            self.int_matrix.set_val(pos[0], pos[1], None)
            for v in voisins:
                if v in self.tested_pos:
                    self.tested_pos.remove(v)

        for v in voisins:
            if self.int_matrix.get_val(*v) is not None:
                self.recUncarve(v)

    def __detRegionsProches(self, c):
        # -- traitement basique : lister les codes distincts des régions voisines
        m_size = self.int_matrix.get_size()
        voisins = cell_voisinnes(c, m_size)
        ens_tmp = set()
        for v in voisins:
            tmp_val = self.int_matrix.get_val(*v)
            if tmp_val is not None:
                ens_tmp.add(tmp_val)
        return list(ens_tmp)

    def __canBeConnector(self, pos):
        # un connecteur : est avant tt un mur, il doit letre
        tmp_val = self.int_matrix.get_val(*pos)
        if tmp_val is not None:
            return False

        # un connecteur : est proche de 2 régions distinctes
        codes_reg_prox = self.__detRegionsProches(pos)
        return len(codes_reg_prox) >= 2

    def __isCloseToRegion(self, pos, code):
        codes_reg_prox = self.__detRegionsProches(pos)
        return code in codes_reg_prox

    def canMerge(self):
        return len(self.candidats_connexion) > 0

    def stepMerge(self):
        COEFF_REDONDANCE = 0.3

        connect_valid = random.choice(self.candidats_connexion)
        tmp = self.__detRegionsProches(connect_valid)

        if tmp[0] in self.all_room_codes:  # on privilegie un connecteur = region de couloir
            args = [tmp[1], tmp[0]]
        else:
            args = tmp

        self.__mergeRegions(connect_valid, args[0], args[1])

        # --- On garde que les connecteurs utiles et pas trop près dun connecteur validé
        liste_filtree = list()

        for c in self.candidats_connexion:
            # -- élimination des connecteurs trop proches du nouveau connect_valid
            if dist_manhattan(c, connect_valid) <= 1:
                continue

            # -- utile pr merger?
            merging_utility = False
            cod_rp = self.__detRegionsProches(c)
            if (cod_rp[0] not in self.regions_to_blobs) or (cod_rp[1] not in self.regions_to_blobs):
                merging_utility = True
            elif self.regions_to_blobs[cod_rp[0]] != self.regions_to_blobs[cod_rp[1]]:
                merging_utility = True

            if merging_utility:
                liste_filtree.append(c)
                continue
            # -- conservation "chanceuse" de candidats inutiles
            if random.random() < COEFF_REDONDANCE:
                liste_filtree.append(c)

        self.candidats_connexion = liste_filtree

    def __findCloseWalls(self, i, j):
        murs_voisins = list()
        for d in DIRS:
            tmp = (i + COORD_OFFSET[d][0], j + COORD_OFFSET[d][1])
            if self.int_matrix.get_val(*tmp) is None:
                murs_voisins.append(tmp)
        return murs_voisins

    def __mergeRegions(self, current_cell, cod_region_a, cod_region_b):
        self.int_matrix.set_val(current_cell[0], current_cell[1], cod_region_a)

        self.candidats_connexion.remove(current_cell)
        self.li_connecteurs.append(current_cell)

        candidats_blob = list()
        if cod_region_a in self.regions_to_blobs:
            candidats_blob.append(self.regions_to_blobs[cod_region_a])
        if cod_region_b in self.regions_to_blobs:
            candidats_blob.append(self.regions_to_blobs[cod_region_b])

        if len(candidats_blob) == 0:
            # nouveau blob
            tmp_blob_codes = list(self.regions_to_blobs.values())
            if len(tmp_blob_codes) == 0:
                blob_corresp = 1
            else:
                blob_corresp = max(tmp_blob_codes) + 1
        else:
            # blob existant, on garde le num le plus petit
            blob_corresp = min(candidats_blob)

        self.regions_to_blobs[cod_region_a] = blob_corresp
        self.regions_to_blobs[cod_region_b] = blob_corresp

    def getMatrix(self):
        return self.int_matrix

    def __startRegion(self):
        self.curr_region += 1

    def getRegion(self):
        return self.curr_region

    def __add_room(self):
        taille_room = random.choice(self.room_possib_size)
        w, h = self.int_matrix.get_size()

        bsupw = w - taille_room
        bsuph = h - taille_room

        intervalle_x = [2 * x + 1 for x in range(0, bsupw // 2)]
        intervalle_y = [2 * y + 1 for y in range(0, bsuph // 2)]
        intervalle_x.pop()
        intervalle_y.pop()

        pos_salle = (
            random.choice(intervalle_x),
            random.choice(intervalle_y)
        )

        # salle empiete sur qq chose ?
        for i in range(pos_salle[0] - 1, pos_salle[0] + taille_room + 2):
            for j in range(pos_salle[1] - 1, pos_salle[1] + taille_room + 2):
                if self.int_matrix.get_val(i, j) is not None:
                    return

        # --- création room
        self.__startRegion()
        code = self.getRegion()
        self.li_rooms.append((pos_salle, taille_room, code))

        for i in range(pos_salle[0], pos_salle[0] + taille_room):
            for j in range(pos_salle[1], pos_salle[1] + taille_room):
                self.int_matrix.set_val(i, j, code)
        self.nb_rooms += 1
        self.all_room_codes.add(code)

    def __carve(self, pos):
        self.int_matrix.set_val(pos[0], pos[1], self.getRegion())

    def __canCarve(self, from_pos, direction):
        base_offset = COORD_OFFSET[direction]
        # on dépasse de la matr?
        offset = map(lambda x: x * 3, base_offset)
        offset = tuple(offset)
        dest = (from_pos[0] + offset[0], from_pos[1] + offset[1])

        m_size = self.int_matrix.get_size()
        if not cell_in_range(dest, m_size):
            return False

        # on tente de carve de deja carvé?
        offset = map(lambda x: x * 2, base_offset)
        offset = tuple(offset)
        dest = (from_pos[0] + offset[0], from_pos[1] + offset[1])
        return self.int_matrix.get_val(*dest) is None

    def __growMaze(self, pos):
        lastDir = None
        WINDING_FACTOR = 0.4

        self.__startRegion()
        self.__carve(pos)
        total_cases_couloir = 1
        SEUIL_CASES = 44

        self.li_cells_to_explore = [pos]

        while len(self.li_cells_to_explore) > 0:

            index_last = len(self.li_cells_to_explore)
            cell = self.li_cells_to_explore[index_last - 1]

            unmade_possib = list()

            for d in DIRS:
                if self.__canCarve(cell, d):
                    unmade_possib.append(d)

            if len(unmade_possib) > 0:
                if lastDir is None:
                    direction = random.choice(unmade_possib)
                else:
                    if (lastDir not in unmade_possib) or (random.random() < WINDING_FACTOR):
                        direction = random.choice(unmade_possib)
                    else:
                        direction = lastDir

                base_offset = COORD_OFFSET[direction]
                self.__carve((cell[0] + base_offset[0], cell[1] + base_offset[1]))
                cell_creusee = (cell[0] + 2 * base_offset[0], cell[1] + 2 * base_offset[1])
                self.__carve(cell_creusee)
                total_cases_couloir += 2
                if total_cases_couloir > SEUIL_CASES:
                    return

                self.li_cells_to_explore.append(cell_creusee)
                lastDir = direction

            else:
                del self.li_cells_to_explore[index_last - 1]
                lastDir = None  # this path ended
