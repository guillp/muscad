"""This contains parts for all kind of threaded or smooth rods and associated nuts."""
from muscad import Cylinder
from muscad import Part


class BrassNut(Part):
    def init(
        self,
        large_cylinder,
        long_cylinder,
        bolt,
        bolt_radius,
        holes=(0, 1, 2, 3),
    ):
        self.large_cylinder = large_cylinder
        self.long_cylinder = long_cylinder.misc()
        self.bolts = (
            sum(bolt.rightward(bolt_radius).z_rotate(90 * i) for i in holes)
            .align(bottom=self.large_cylinder.bottom)
            .misc()
        )

    @classmethod
    def T8(cls, bolt=None, T=0.2):
        large_cylinder = Cylinder(d=22 + 2 * T, h=3.5 + 2 * T)
        long_cylinder = Cylinder(d=10.2 + 2 * T, h=15 + 2 * T).down(1.5)
        return cls(large_cylinder, long_cylinder, bolt, 8)


class Rod(Part):
    def init(self, diameter, length):
        self.rod = Cylinder(d=diameter, h=length)

    @classmethod
    def d8(cls, length=300, T=0.2):
        return cls(diameter=8 + 2 * T, length=length)

    @classmethod
    def d10(cls, length=300, T=0.2):
        return cls(diameter=10 + 2 * T, length=length)

    @classmethod
    def d12(cls, length=300, T=0.2):
        return cls(diameter=12 + 2 * T, length=length)


class ThreadedRod(Part):
    def init(self, diameter, length):
        self.rod = Cylinder(d=diameter, h=length)

    @classmethod
    def T8(cls, length=300, T=0.2):
        return cls(diameter=8 + 2 * T, length=length)

    def add_brass_nut(self, brass_nut, align=True):
        if align:
            self.brass_nut = brass_nut.align(
                center_x=self.rod.center_x, center_y=self.rod.center_y
            )
        return self
