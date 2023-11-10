"""This contains parts for all kind of threaded or smooth rods and associated nuts."""
from typing import Iterable

from typing_extensions import Self

from muscad import Cylinder, Object, Part, Union


class BrassNut(Part):
    def init(  # type: ignore[override]
        self,
        large_cylinder: Object,
        long_cylinder: Object,
        bolt: Object,
        bolt_radius: float,
        holes: Iterable[int] = (0, 1, 2, 3),
    ) -> None:
        self.large_cylinder = large_cylinder
        self.long_cylinder = long_cylinder.misc()
        self.bolts = (
            Union(bolt.rightward(bolt_radius).z_rotate(90 * i) for i in holes)
            .align(bottom=self.large_cylinder.bottom)
            .misc()
        )

    @classmethod
    def T8(cls, bolt: Object, T: float = 0.2) -> Self:
        large_cylinder = Cylinder(d=22 + 2 * T, h=3.5 + 2 * T)
        long_cylinder = Cylinder(d=10.2 + 2 * T, h=15 + 2 * T).down(1.5)
        return cls(large_cylinder, long_cylinder, bolt, 8)


class Rod(Part):
    def init(self, diameter: float, length: float) -> None:  # type: ignore[override]
        self.rod = Cylinder(d=diameter, h=length)

    @classmethod
    def d8(cls, length: float = 300, T: float = 0.2) -> Self:
        return cls(diameter=8 + 2 * T, length=length)

    @classmethod
    def d10(cls, length: float = 300, T: float = 0.2) -> Self:
        return cls(diameter=10 + 2 * T, length=length)

    @classmethod
    def d12(cls, length: float = 300, T: float = 0.2) -> Self:
        return cls(diameter=12 + 2 * T, length=length)


class ThreadedRod(Part):
    def init(self, diameter: float, length: float) -> None:  # type: ignore[override]
        self.rod = Cylinder(d=diameter, h=length)

    @classmethod
    def T8(cls, length: float = 300, T: float = 0.2) -> Self:
        return cls(diameter=8 + 2 * T, length=length)

    def add_brass_nut(self, brass_nut: Object, *, align: bool = True) -> Self:
        if align:
            self.brass_nut = brass_nut.align(
                center_x=self.rod.center_x, center_y=self.rod.center_y
            )
        return self
