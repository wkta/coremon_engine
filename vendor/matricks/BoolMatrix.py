from matricks.BaseMatrix import BaseMatrix


class BoolMatrix(BaseMatrix):
    # --- redefinition de 2 methodes venant den haut
    @classmethod
    def defaultValue(cls):
        return True

    @classmethod
    def isValidValue(cls, val):
        return isinstance(val, bool)
