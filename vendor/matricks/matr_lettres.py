from tools.BaseMatrix import BaseMatrix


class MatrLettres(BaseMatrix):
    COD_A = ord('a')
    COD_Z = ord('z')

    # --- redefinition 2 methodes venant den haut
    @classmethod
    def defaultValue(cls):
        return 'a'

    @classmethod
    def isValidValue(cls, val):
        cod = ord(val)
        if cls.COD_A <= cod <= cls.COD_Z:
            return True
        return False

kk = MatrLettres((7, 6))
kk.setValue(0, 1, 'o')
kk.setValue(0, 2, 'k')
kk.setValue(1, 0, 'm')
kk.setValue(2, 0, 'a')
kk.setValue(3, 0, 'n')
print(' 0 0 porte ' + str(kk.getValue(0, 0)))
print(' 3 0 porte ' + str(kk.getValue(3, 0)))

print('affiche matr entière')
print(str(kk))
