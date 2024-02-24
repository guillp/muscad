from __future__ import annotations

import contextlib

from muscad import Cylinder, E, Hole, Misc, Object, Part, calc


class Tube(Part):
    def init(  # type: ignore[override]
        self,
        diameter: float | None = None,
        *args: Misc | Hole | Object,
        radius: float | None = None,
        top_diameter: float | None = None,
        top_radius: float | None = None,
        left: float | None = None,
        center_x: float | None = None,
        right: float | None = None,
        width: float | None = None,
        back: float | None = None,
        center_y: float | None = None,
        front: float | None = None,
        depth: float | None = None,
        bottom: float | None = None,
        center_z: float | None = None,
        top: float | None = None,
        height: float | None = None,
        segments: int | None = None,
        **kwargs: Misc | Hole | Object,
    ) -> None:
        match diameter, radius:
            case None, None:
                # no explicit diameter or radius, try to deduce it from the other params
                with contextlib.suppress(ValueError):
                    left, center_x, right, width = calc(left, center_x, right, width)
                with contextlib.suppress(ValueError):
                    back, center_y, front, depth = calc(back, center_y, front)
                match width, depth:
                    case None, None:
                        msg = (
                            "No sufficient parameter to calculate the barrel diameter."
                            " Please provide either a diameter `d`, a radius `r`,"
                            "or at least 2 two parameters on axis X or Y."
                        )
                        raise ValueError(msg)
                    case float() | int(), None:
                        diameter = width
                    case None, float() | int():
                        diameter = depth
                    case float() | int(), float() | int() if width != depth:
                        msg = (
                            f"width ({width}mm) is different from depth ({depth}mm)."
                            " I don't know which one to use as diameter."
                        )
                        raise ValueError(msg)
            case float() | int(), None if diameter is not None:
                pass
            case None, float() if radius is not None:
                diameter = radius * 2
            case (
                float()
                | int(),
                float()
                | int(),
            ) if radius is not None and diameter is not None and radius * 2 != diameter:
                msg = (
                    "diameter `d` and radius `r` must be consistent." "Please fix, or provide either one or the other."
                )
                raise ValueError(msg)

        assert diameter is not None

        match top_radius, top_diameter:
            case None, float() | int():
                pass
            case float() | int(), None if top_radius is not None:
                top_diameter = top_radius * 2
            case (
                float()
                | int(),
                float()
                | int(),
            ) if top_diameter is not None and top_radius is not None and top_diameter != top_radius * 2:
                msg = (
                    f"inconsistent top diameter `d2` ({top_diameter}mm) and top radius ({top_radius}mm)."
                    "Please fix, or provide either one or the other."
                )
                raise ValueError(msg)

        match width, diameter:
            case None, float() | int():
                width = diameter
            case float() | int(), float() | int() if width != diameter:
                msg = f"diameter `d` ({diameter}mm) is different from width ({width}mm)."
                raise ValueError(msg)

        match depth, diameter:
            case None, float() | int():
                depth = diameter
            case float() | int(), None:
                assert False
            case float() | int(), float() | int() if depth != diameter:
                msg = f"diameter `d` ({diameter}mm) is different from depth ({depth}mm)."
                raise ValueError(msg)

        left, center_x, right, width = calc(left, center_x, right, width)
        back, center_y, front, depth = calc(back, center_y, front, depth)
        bottom, center_z, top, height = calc(bottom, center_z, top, height)
        self.cylinder = Cylinder(d=diameter, d2=top_diameter, h=height, segments=segments).align(
            center_x=center_x, center_y=center_y, center_z=center_z
        )
        super().init(*args, **kwargs)

    def tunnel(self, diameter: float | None = None, radius: float | None = None) -> Tube:
        """Hollows the center of this tube, making it a tunnel."""
        if diameter is None:
            if radius is None:
                msg = "at least one of diameter or radius must be specified"
                raise ValueError(msg)
            diameter = radius * 2
        self.tunnel_hole = ~Cylinder(d=diameter, h=self.height + 2).align(
            center_x=self.center_x,
            center_y=self.center_y,
            center_z=self.center_z,
        )
        return self

    def add_corner(
        self,
        angle: float = 0,
        right_distance: float = 0,
        front_distance: float = 0,
        bottom_distance: float = 0,
        top_distance: float = 0,
    ) -> Tube:
        """Turns a quarter of this tube into a cube."""
        from muscad import Volume

        self.add_misc(
            Volume(
                left=self.center_x,
                right=self.right + right_distance,
                back=self.center_y,
                front=self.front + front_distance,
                bottom=self.bottom + bottom_distance,
                top=self.top + top_distance,
            ).z_rotate(angle, center_x=self.center_x, center_y=self.center_y)
        )
        return self

    def cut_corner(self, angle: float = 0) -> Tube:
        """Removes a quarter of this tube."""
        from muscad import Volume

        self.add_hole(
            Volume(
                left=self.center_x,
                right=self.right,
                back=self.center_y,
                front=self.front - E,
                bottom=self.bottom + E,
                top=self.top,
            ).z_rotate(angle)
        )
        return self

    def add_side(self, angle: float = 0, distance: float = 0) -> Tube:
        """Turns a quarter of this tube into a cube."""
        from muscad import Volume

        self.add_misc(
            Volume(
                left=self.center_x,
                right=self.right + distance,
                back=self.back,
                front=self.front,
                bottom=self.bottom,
                top=self.top,
            ).z_rotate(angle)
        )
        return self
