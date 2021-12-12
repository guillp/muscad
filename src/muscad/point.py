from muscad.helpers import atan2
from muscad.helpers import cos
from muscad.helpers import radians
from muscad.helpers import sin


class Vector:
    """A helper class that keeps some ordered, named coordinates."""

    def __init__(self, **kwargs: float):
        self.kwargs = kwargs

    def __getattr__(self, item: str) -> float:
        return self.kwargs[item]

    def __str__(self) -> str:
        return str([round(i, 4) if i != 0.0 else 0 for i in self.kwargs.values()])


class Point2D(Vector):
    """A 2D Point with x and y coordinates."""

    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y)

    def z_rotate(self, angle: float) -> "Point2D":
        return Point2D(
            cos(angle) * self.x + sin(angle) * self.y,
            cos(angle) * self.y - sin(angle) * self.x,
        )

    def x_mirror(self) -> "Point2D":
        return Point2D(-self.x, self.y)

    def y_mirror(self) -> "Point2D":
        return Point2D(self.x, -self.y)

    def opposite(self) -> "Point2D":
        return Point2D(-self.x, -self.y)

    def angle(self) -> float:
        return atan2(self.y, self.x)

    @classmethod
    def from_radius_and_angle(cls, radius: float, angle: float) -> "Point2D":
        return cls(radius * cos(angle), radius * sin(angle))

    @classmethod
    def involute(cls, radius: float, angle: float) -> "Point2D":
        return cls(
            radius * (cos(angle) + radians(angle) * sin(angle)),
            radius * (sin(angle) - radians(angle) * cos(angle)),
        )

    def to_3d(self, z: float = 0) -> "Point3D":
        """Turns this Point2D into a Point3D"""
        return Point3D(self.x, self.y, z)


class Point3D(Vector):
    """A 3D point with x, y and z coordinates."""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x=x, y=y, z=z)
