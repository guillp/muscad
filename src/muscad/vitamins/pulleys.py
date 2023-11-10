"""A port of https://www.thingiverse.com/thing:16627 in MuSCAD."""
from typing_extensions import Self

from muscad import EE, Cube, Cylinder, Object, Part, Polygon, Union


class Pulley(Part):
    def init(  # type: ignore[override]
        self,
        outer_dia: float,  # outer diameter of the thooted part
        height: float,  # height of the thooted part
    ) -> None:
        self.body = Cylinder(d=outer_dia, h=height)

    def tooth(self, profile: Polygon, count: int) -> Self:
        self._tooth = ~Union(
            profile.linear_extrude(height=self.body.height - EE)
            .align(back=self.body.back, center_z=self.body.center_z)
            .z_rotate(360 / count * i)
            for i in range(count)
        )
        return self

    def add_flange(
        self, diameter: float, *, height: float, top: bool = True, bottom: bool = True
    ) -> Self:
        if height > 0 and top:
            self.top_flange = Cylinder(d=diameter, h=height).align(
                center_x=self.body.center_x,
                center_y=self.body.center_y,
                bottom=self.body.top,
            )
        if height > 0 and bottom:
            self.bottom_flange = Cylinder(d=diameter, h=height).align(
                center_x=self.body.center_x,
                center_y=self.body.center_y,
                top=self.body.bottom,
            )
        return self

    def add_bolt(self, bolt: Object, z_offset: float = 0) -> Self:
        self.bolt = bolt.align(center_z=self.center_z).z_translate(z_offset).misc()
        return self

    def add_clearance(self, length: float, angle: float) -> Self:
        self.clearance = (
            Cube(self.body.width, length, self.body.height)
            .align(
                center_x=self.body.center_x,
                back=self.body.center_y,
                center_z=self.body.center_z,
            )
            .z_rotate(angle)
            .misc()
        )
        return self

    def add_belt_clearance(
        self, length: float, *, angle: float, left: bool = False
    ) -> Self:
        self.belt_clearance = (
            Cube(self.body.width / 2, length, self.body.height)
            .align(
                left=self.body.left if left else self.body.center_x,
                back=self.body.center_y,
                center_z=self.body.center_z,
            )
            .z_rotate(angle)
            .misc()
        )
        return self

    def add_shaft_clearance(
        self, d: float = 5, lenght: float = 20, T: float = 0.2, **align: float
    ) -> Self:
        self.shaft = Cylinder(d=d + 2 * T, h=lenght).align(**align).misc()
        return self

    @classmethod
    def GT2(
        cls, tooth_count: int, height: float = 6, shaft_dia: float = 3, T: float = 0.2
    ) -> Self:
        if tooth_count < 10:
            msg = "Unable to draw a GT2 pulley with less than 10 tooth"
            raise ValueError(msg)
        outer_dia = tooth_outer_diameter(tooth_count, 2, 0.254)
        return cls(outer_dia, height).add_shaft_clearance(shaft_dia, T=T)

    @classmethod
    def placeholder(cls, diameter: float, height: float, T: float = 0.2) -> Self:
        return cls(outer_dia=diameter + 2 * T, height=height + 2 * T)


def tooth_outer_diameter(
    tooth_count: int, tooth_pitch: float, pitch_line_offset: float
) -> float:
    return 2 * ((tooth_count * tooth_pitch) / (3.141_592_65 * 2) - pitch_line_offset)
