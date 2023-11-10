from __future__ import annotations

from muscad.utils.tube import Tube


class CableChain:
    @classmethod
    def female(
        cls, outer_diameter: float = 16, inner_diameter: float = 6, T: float = 0.2
    ) -> Tube:
        return Tube(diameter=outer_diameter - T, bottom=T, top=1 - T).tunnel(
            inner_diameter + T
        )

    @classmethod
    def male(
        cls,
        outer_diameter: float = 16,
        inner_diameter: float = 6,
        shaft_length: float = 5,
        T: float = 0.2,
    ) -> Tube:
        if shaft_length > 0:
            clearance = Tube(
                diameter=outer_diameter + T,
                bottom=2 - T,
                height=shaft_length + T,
            ).tunnel(inner_diameter - 2 * T)
        else:
            clearance = Tube(
                diameter=outer_diameter + 2 * T,
                top=abs(shaft_length),
                height=-shaft_length + T,
            ).tunnel(inner_diameter - 2 * T)
        return Tube(
            diameter=outer_diameter - T,
            bottom=0,
            height=abs(shaft_length) + 2 - T,
            clearance=~clearance,
        )

    @classmethod
    def couple(
        cls, outer_diameter: float = 16, inner_diameter: float = 6, T: float = 0.2
    ) -> tuple[Tube, Tube]:
        return cls.female(outer_diameter, inner_diameter, T), cls.male(
            outer_diameter, inner_diameter, T
        )
