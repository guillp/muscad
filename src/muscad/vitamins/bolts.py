"""A Nut and Bolts library.

Some measurements are taken from the MCAD library at
https://github.com/SolidCode/MCAD/blob/master/nuts_and_bolts.scad

"""
from typing_extensions import Self

from muscad import Cube, Cylinder, E, Hull
from muscad.part import Part


class Nut(Part):
    def init(self, width: float, thickness: float, segments: int = 6) -> None:  # type: ignore[override]
        self._width = width
        self._thickness = thickness
        self.nut = Cylinder(d=width, h=thickness, segments=segments)

    @classmethod
    def M3(cls, T: float = 0.2) -> Self:
        return cls(6.4 + 2 * T, 2.4 + 2 * T)


class Bolt(Part):
    def init(  # type: ignore[override]
        self,
        diameter: float,
        length: float,
        head_height: float,
        head_diameter: float,
        nut_diameter: float,
        head_clearance: float = 0,
        head: bool = True,
        thread_clearance: float = 0,
    ) -> None:
        self.thread = Cylinder(d=diameter, h=length)
        if thread_clearance:
            self.tread_clearance = (
                Cylinder(d=diameter, h=thread_clearance)
                .align(bottom=self.thread.top)
                .misc()
            )
        if head:
            self.head = Cylinder(d=head_diameter, h=head_height).align(
                top=self.thread.bottom + E
            )
            if head_clearance:
                self.head_clearance = (
                    Cylinder(d=head_diameter, h=head_clearance)
                    .align(top=self.head.bottom + E)
                    .misc()
                )

        self.diameter = diameter
        self.length = length
        self.head_height = head_height
        self.head_diameter = head_diameter
        self.nut_diameter = nut_diameter

    def add_nut(
        self,
        placement: float = 0,
        inline_clearance_size: float = 0,
        side_clearance_size: float = 0,
        angle: float = 0,
        T: float = 0.2,
    ) -> Self:
        nut_width = self.nut_diameter
        nut_thickness = self.head_height
        if placement < 0:
            placement = self.length + placement - nut_thickness + 0.1

        nut = (
            Nut(nut_width, nut_thickness)
            .align(bottom=self.thread.bottom + placement)
            .z_rotate(angle)
            .misc()
        )
        self.add_misc(nut)
        if inline_clearance_size > 0:
            self.inline_nut_clearance = Hull(
                nut.object, nut.up(inline_clearance_size)
            ).misc()
        if side_clearance_size > 0:
            self.nut_clearance = (
                Cube(
                    side_clearance_size,
                    nut_width / 2 * 3**0.5 + T,
                    nut_thickness,
                )
                .align(
                    left=nut.center_x,
                    center_y=nut.center_y,
                    center_z=nut.center_z,
                )
                .z_rotate(angle)
                .misc()
            )

        return self

    @classmethod
    def M2(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 0,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=1.98 + 2 * T,
            length=length,
            head=head,
            head_height=2.4 + 2 * T,
            head_diameter=3.8 + 2 * T,
            nut_diameter=6.4 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M3(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 0,
        head_height: float = 2.4,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=2.98 + 2 * T,
            length=length,
            head=head,
            head_height=head_height + 2 * T,
            head_diameter=5.5 + 2 * T,
            nut_diameter=6.4 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M4(
        cls,
        length: float,
        *,
        head: bool = True,
        head_height: float = 4,
        head_clearance: float = 0,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=3.978 + 2 * T,
            length=length,
            head=head,
            head_height=head_height + T,
            head_diameter=6.9 + 2 * T,
            nut_diameter=6.9 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M5(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=4.976 + 2 * T,
            length=length,
            head=head,
            head_height=4 + 2 * T,
            head_diameter=9.2 + 2 * T,
            nut_diameter=9.2 + 2 * T,
            head_clearance=head_clearance,
        )

    @classmethod
    def M6(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 0,
        head_height: float = 6,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=5.974 + 2 * T,
            length=length,
            head=head,
            head_height=head_height + 2 * T,
            head_diameter=11.5 + 2 * T,
            nut_diameter=11.5 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M8(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 100,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=7.972 + 2 * T,
            length=length,
            head=head,
            head_height=6.5 + 2 * T,
            head_diameter=15 + 2 * T,
            nut_diameter=15 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M10(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 100,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=9.968 + 2 * T,
            length=length,
            head=head,
            head_height=8 + 2 * T,
            head_diameter=19.6 + 2 * T,
            nut_diameter=19.6 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )

    @classmethod
    def M12(
        cls,
        length: float,
        *,
        head: bool = True,
        head_clearance: float = 100,
        thread_clearance: float = 0,
        T: float = 0.2,
    ) -> Self:
        return cls(
            diameter=11.966 + 2 * T,
            length=length,
            head=head,
            head_height=9 + 2 * T,
            head_diameter=21.5 + 2 * T,
            nut_diameter=21.5 + 2 * T,
            head_clearance=head_clearance,
            thread_clearance=thread_clearance,
        )
