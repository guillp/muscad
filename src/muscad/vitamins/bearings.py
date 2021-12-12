from __future__ import annotations

from typing import Dict
from typing import Optional

from muscad import Cylinder
from muscad import EE
from muscad import Object
from muscad import Part
from muscad import Union
from muscad.utils.volume import Volume
from muscad.vitamins.bolts import Bolt


class LinearBearing(Part):
    def init(
        self, inner_diam: float, outer_diam: float, length: float, hollow: bool = True
    ) -> None:
        self._outer_diam = outer_diam
        self._inner_diam = inner_diam
        self._length = length

        self.outer = Cylinder(d=outer_diam, h=length)
        if hollow:
            self.inner = ~Cylinder(d=inner_diam, h=length * 2)

    def add_throats(
        self, diameter: float, width: float, offset: float
    ) -> LinearBearing:
        throat = Cylinder(d=self._outer_diam + 1, h=width) - Cylinder(
            d=diameter, h=width + 1
        )
        self.left_throat = ~throat.align(bottom=self.outer.bottom + offset)
        self.right_throat = ~throat.align(top=self.outer.top - offset)
        return self

    def add_rod_clearance(self, length: float = 20, T: float = 1) -> LinearBearing:
        self.rod_clearance = Cylinder(
            d=self._inner_diam + 2 * T, h=self._length + 2 * length
        ).misc()
        return self

    @classmethod
    def LM8UU(cls, hollow: bool = True, T: float = 0.2) -> LinearBearing:
        return cls(
            inner_diam=8 + 2 * T,
            outer_diam=15 + 2 * T,
            length=24 + 2 * T,
            hollow=hollow,
        ).add_throats(14 + 2 * T, 1.1 - T, 3.25 + T)

    @classmethod
    def LM12UU(cls, hollow: bool = True, T: float = 0.2) -> LinearBearing:
        return cls(
            inner_diam=12 + 2 * T,
            outer_diam=21 + T,
            length=30.2 + 2 * T,
            hollow=hollow,
        )


class BushingLinearBearing(Part):
    def init(
        self, *, rod_diameter: float, width: float, depth: float, height: float
    ) -> None:
        self.rod_diameter = rod_diameter
        self.base = Volume(
            width=width,
            depth=depth,
            height=height,
            center_x=0,
            center_y=0,
            center_z=0,
        )

    def add_bolts(
        self,
        bolt: Object,
        bolt_distance_width: float,
        bolt_distance_depth: float,
        offset: float = 8,
    ) -> BushingLinearBearing:
        self.bolts = Union(
            bolt.align(
                center_x=self.base.center_x + i * bolt_distance_width / 2,
                center_y=self.base.center_y + j * bolt_distance_depth / 2,
                bottom=self.bottom - offset,
            )
            for i in (-1, 1)
            for j in (-1, 1)
        ).misc()
        return self

    def add_rod_clearance(
        self, length: float = 20, slide: Optional[Dict[str, float]] = None, T: float = 1
    ) -> BushingLinearBearing:
        slide = slide or {}
        self.rod_clearance = (
            Cylinder(d=self.rod_diameter + 2 * T, h=self.width + 2 * length)
            .slide(**slide)
            .x_rotate(90)
            .misc()
        )
        return self

    @classmethod
    def SC8UU(
        cls,
        bolt_len: float = 10,
        bolt_offset: float = 8,
        bolt_head_clearance: float = 0,
        T: float = 0.2,
    ) -> BushingLinearBearing:
        bearing = cls(
            rod_diameter=8,
            width=34 + 2 * T,
            depth=30 + 2 * T,
            height=22 + 2 * T,
        )
        bearing.add_bolts(
            bolt_distance_width=24,
            bolt_distance_depth=18,
            bolt=Bolt.M4(bolt_len, head_clearance=bolt_head_clearance, T=T),
            offset=bolt_offset - T,
        )
        return bearing

    @classmethod
    def SC12UU(
        cls,
        bolt_len: float = 12,
        bolt_offset: float = 8,
        bolt_head_clearance: float = 0,
        T: float = 0.2,
    ) -> BushingLinearBearing:
        bearing = cls(
            rod_diameter=12,
            width=42 + 2 * T,
            depth=36 + 2 * T,
            height=28 + 2 * T,
        )
        bearing.add_bolts(
            bolt_distance_width=30.5,
            bolt_distance_depth=26,
            bolt=Bolt.M4(bolt_len, head_clearance=bolt_head_clearance, T=T),
            offset=bolt_offset,
        )
        return bearing


class RotationBearing(Part):
    def init(
        self, inner_diam: float, outer_diam: float, height: float, hole: bool = True
    ) -> None:
        self._outer_diameter = outer_diam
        self._inner_diameter = inner_diam
        self._height = height

        self.outer = Cylinder(d=outer_diam, h=height)
        if hole:
            self.inner = ~Cylinder(d=inner_diam, h=height + EE)

    @classmethod
    def b605zz(cls, T: float = 0.2, hole: bool = True) -> RotationBearing:
        return cls(5 + 2 * T, 14 + 2 * T, 5 + 2 * T, hole=hole)

    @classmethod
    def b608zz(cls, T: float = 0.2, hole: bool = True) -> RotationBearing:
        return cls(8 + 2 * T, 22 + 2 * T, 7 + 2 * T, hole=hole)

    def add_clearance(self, size: float) -> RotationBearing:
        self.clearance = ~(
            Cylinder(d=self._outer_diameter + size, h=self._height) - self.inner
        )
        return self
