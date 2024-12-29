"""The Shape class, which contains helpers for commonly used 3D Shapes."""

from muscad import EE, Cylinder, Object


class Shape:
    @classmethod
    def pipe(
        cls,
        height: float,
        outer_diameter: float,
        inner_diameter: float,
    ) -> Object:
        return Cylinder(d=outer_diameter, h=height) - Cylinder(d=inner_diameter, h=height + EE)

    @classmethod
    def cone(cls, height: float, diameter: float) -> Object:
        return Cylinder(d=diameter, d2=0, h=height)

    @classmethod
    def oval_prism(cls, height: float, x_diameter: float, y_diameter: float) -> Object:
        return Cylinder(h=height, d=y_diameter).scale(y=x_diameter / y_diameter)

    @classmethod
    def oval_tube(cls, height: float, x_diameter: float, y_diameter: float, wall: float) -> Object:
        return Cylinder(h=height, d=x_diameter).scale(y=y_diameter / x_diameter) - Cylinder(
            h=height + EE, d=x_diameter
        ).scale(
            x=(x_diameter - wall * 2) / x_diameter,
            y=(y_diameter - wall * 2) / x_diameter,
        )
