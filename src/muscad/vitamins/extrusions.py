from muscad import Circle
from muscad import Hull
from muscad import Part
from muscad import Square
from muscad import Surface
from muscad import TT
from muscad import Volume


class Extrusion(Part):
    def init(self, side, length, rounding=2):
        self.profile = Hull(
            Circle(d=rounding * 2).align(left=-side / 2, back=-side / 2),
            Circle(d=rounding * 2).align(left=-side / 2, front=side / 2),
            Circle(d=rounding * 2).align(right=side / 2, back=-side / 2),
            Circle(d=rounding * 2).align(right=side / 2, front=side / 2),
        ).z_linear_extrude(length)

    @classmethod
    def e3030(cls, length, rounding=2, T=0.1):
        return cls(30 + 2 * T, length, rounding)

    @classmethod
    def e2020(cls, length, rounding=2, T=0.1):
        return cls(20 + 2 * T, length, rounding)


class Extrusion3030Insert(Part):
    def init(self, length=50):
        self.body = Volume(width=8 - TT, depth=length, height=6).fillet_depth(
            0.5, bottom=True
        )
        self.wings = Surface.free(
            Circle(d=1.5, segments=20).align(center_x=6, back=-0.5),
            Circle(d=1.5, segments=20).align(center_x=-6, back=-0.5),
            Square(width=8, depth=1).align(center_x=0, front=3),
        ).y_linear_extrude(length)
