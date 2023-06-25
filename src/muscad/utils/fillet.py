from muscad import EE, Circle, E, Part, Square, cos, sin


class Fillet(Part):
    def init(self, radius: float = 4) -> None:  # type: ignore[override]
        self.box = Square(radius + EE, radius + EE).align(back=-E, left=-E, center_z=0)
        self.fillet = ~Circle(d=radius * 2)


class Chamfer(Part):
    def init(self, radius: float = 4, angle: float = 45) -> None:  # type: ignore[override]
        self.box = Square(radius + EE, radius + EE).align(back=-E, left=-E, center_z=0)
        if angle == 45:
            chamfer_width = (radius**2 * 2) ** 0.5
            self.chamfer = ~Square(chamfer_width, chamfer_width + 1).z_rotate(angle)
        else:
            chamfer_width = (
                (radius * cos(angle)) ** 2 + (radius * sin(angle)) ** 2
            ) ** 0.5
            self.chamfer = ~Square(chamfer_width, chamfer_width).z_rotate(
                angle, center_x=-cos(45 + angle), center_y=-cos(angle)
            )
