import math


class Vector2d:
    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = float(x), float(y)

    @classmethod
    def new_from_angle(cls, theta):
        coord_x = math.cos(theta)
        coord_y = math.sin(theta)
        return cls(coord_x, coord_y)

    def get_int_coords(self):
        return int(self.x), int(self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def avec_magnitude(self, longueur_voulue):
        """
        :return: un nouveau obj type Vecteur2, conservant l'orientation actuelle, ayant une magnitude donnee
        """
        res = self.clone()
        res.normalize()
        res.multiply(longueur_voulue)
        return res

    def normalize(self):
        lg = self.length()
        if lg != 0:
            self.x = float(self.x) / lg
            self.y = float(self.y) / lg

    def multiply(self, facteur):
        self.x *= facteur
        self.y *= facteur

    def clone(self):
        return self.__class__(self.x, self.y)

    def __add__(self, other_vect):
        return self.__class__(self.x + other_vect.x, self.y + other_vect.y)
