from __future__ import annotations

from muscad import Cylinder, E, Hole, Misc, Object, Part, Volume, calc


class Tube(Part):
    def init(  # type: ignore[override]
        self,
        *args: Misc | Hole | Object,
        diameter: float | None = None,
        top_diameter: float | None = None,
        radius: float | None = None,
        left: float | None = None,
        center_x: float | None = None,
        right: float | None = None,
        back: float | None = None,
        center_y: float | None = None,
        front: float | None = None,
        bottom: float | None = None,
        center_z: float | None = None,
        top: float | None = None,
        height: float | None = None,
        **kwargs: Misc | Hole | Object,
    ) -> None:
        if diameter is None and radius is not None:
            diameter = radius * 2
        try:
            # first try to get the cylinder diameter from the x coordinates
            left, center_x, right, diameter = calc(left, center_x, right, diameter)
        except ValueError:
            pass

        # fallback to the y coordinates
        back, center_y, front, diameter = calc(back, center_y, front, diameter)

        bottom, center_z, top, height = calc(bottom, center_z, top, height)
        self.cylinder = Cylinder(d=diameter, d2=top_diameter, h=height).align(
            center_x=center_x, center_y=center_y, bottom=bottom
        )
        super().init(*args, **kwargs)

    def tunnel(
        self, diameter: float | None = None, radius: float | None = None
    ) -> Tube:
        """Hollows the center of this tube, making it a tunnel."""
        if diameter is None and radius is None:
            raise ValueError("at least one of diameter or radius must be specified")
        if diameter is None and radius is not None:
            diameter = radius * 2
        if diameter is None:
            raise ValueError("this is just to make mypy happy")
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
