from muscad import Circle, Part, Square


class Lauburu(Part):
    # base = Import("lauburu.stl").scale(x=2, y=2, z=.1).background()

    def init(self, r: float = 100, width: float = 10) -> None:  # type: ignore[override]
        shape = (
            Circle(d=r / 2).align(center_x=r * 0.75 + width, center_y=0)
            + (
                Circle(d=r + width).align(center_x=(r + width) / 2, center_y=0)
                - Circle(d=r / 2).align(center_x=r * 0.25 + width, center_y=0)
                & Square(r + width * 2, r).align(left=0, back=0)
            )
        ).offset(r=0.4, invert=True)
        self.cutter = shape.z_linear_extrude(6)
        self.wing = shape.offset(1).z_linear_extrude(5).align(bottom=self.cutter.top)
        self.reinforcement = (
            shape.offset(3).z_linear_extrude(3).align(bottom=self.wing.top)
        )


if __name__ == "__main__":
    Lauburu().render_to_file()
