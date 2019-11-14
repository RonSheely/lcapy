from .symbols import s
from .immitance import Immitance

class Impedance(Immitance):
    """Generic impedance class."""

    @property
    def Yw(self):
        return 1 / self.Zw

    @property
    def Zw(self):
        return self.jomega

    def cpt(self):
        from .oneport import R, C, L, Z

        if self.is_number or self.is_dc:
            return R(self.expr)

        z = self * s

        if z.is_number:
            return C((1 / z).expr)

        z = self / s

        if z.is_number:
            return L(z.expr)

        return Z(self)
    

