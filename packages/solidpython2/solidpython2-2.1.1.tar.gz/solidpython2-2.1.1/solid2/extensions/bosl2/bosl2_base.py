from solid2.core.object_base.object_base_impl import BareOpenSCADObject
from solid2.core.object_base.operator_mixin import OperatorMixin
from solid2.extensions.bosl2.bosl2_access_syntax_mixin import Bosl2AccessSyntaxMixin


class Bosl2OperatorMixin(OperatorMixin):
    def __add__(self, x): #type: ignore
        from .std import union
        return self._union_op(x, union)

    def __or__(self, x): #type: ignore
        from .std import union
        return self._union_op(x, union)

    def __radd__(self, x): #type: ignore
        from .std import union
        return self._union_op(x, union)

    def __sub__(self, x): #type: ignore
        from .std import difference
        return self._difference_op(x, difference)

    def __mul__(self, x): #type: ignore
        from .std import intersection
        return self._intersection_op(x, intersection)

    def __and__(self, x): #type: ignore
        from .std import intersection
        return self._intersection_op(x, intersection)


class Bosl2Base(Bosl2AccessSyntaxMixin, Bosl2OperatorMixin, BareOpenSCADObject):
    # flip back & fwd -> issue #54
    # https://github.com/jeff-dh/SolidPython/issues/54
    # def back(self, y=None, p=None, **kwargs): #type: ignore
    #     return Bosl2AccessSyntaxMixin.fwd(self, y, p, *kwargs)
    #
    # def fwd(self, y=None, p=None, **kwargs): #type: ignore
    #     return Bosl2AccessSyntaxMixin.back(self, y, p, *kwargs)
    #
    pass
