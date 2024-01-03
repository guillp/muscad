from muscad import Part


class Star(Part):
    def init(self, part: Part, n: int) -> None:  # type: ignore[override]
        for i in range(n):
            self.add_child(part.z_rotate(i * 360 / n))
