from matricks.BaseMatrix import BaseMatrix


class IntegerMatrix(BaseMatrix):
    """
    modélise une matrice d'entiers. Par défaut, toutes les cellules sont à 0
    """

    # --- redefinition de 2 methodes venant den haut
    @classmethod
    def defaultValue(cls):
        return None  # TODO faire en sorte que ce soit 0 mais faudra modifer RandomMaze avant cela

    @classmethod
    def isValidValue(cls, val):
        return (val is None) or isinstance(val, int)
