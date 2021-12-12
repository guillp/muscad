"""This modules contains 2D & 3D Primitives classes that match OpenSCAD primitives."""
import os
import sys
import typing
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from muscad.base import Primitive
from muscad.point import Point2D
from muscad.point import Point3D


class Cube(Primitive):
    """OpenSCAD's `cube`."""

    def __init__(self, width: float, depth: float, height: float) -> None:
        super().__init__()
        self._width = width
        self._depth = depth
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def height(self) -> float:
        return self._height

    @property
    def left(self) -> float:
        return -self.width / 2

    @property
    def back(self) -> float:
        return -self.depth / 2

    @property
    def bottom(self) -> float:
        return -self.height / 2

    @property
    def right(self) -> float:
        return self.width / 2

    @property
    def front(self) -> float:
        return self.depth / 2

    @property
    def top(self) -> float:
        return self.height / 2

    def _arguments(self) -> Dict[str, Any]:
        return {
            "size": Point3D(self._width, self._depth, self._height),
            "center": True,
        }


class Cylinder(Primitive):
    def __init__(
        self,
        h: float,
        d: float,
        d2: Optional[float] = None,
        segments: Optional[int] = None,
    ):
        super().__init__()
        self._height = h
        self.diameter = d
        self.top_diameter = d2
        if segments is None:
            segments = int(d * 3.14 / 0.4)
        self.segments = segments

    def _arguments(self):
        if self.top_diameter is None:
            return {
                "h": self._height,
                "d": self.diameter,
                "$fn": self.segments,
                "center": True,
            }
        return {
            "h": self._height,
            "d1": self.diameter,
            "d2": self.top_diameter,
            "$fn": self.segments,
            "center": True,
        }

    @property
    def width(self):
        return max(self.diameter, self.top_diameter or 0)

    @property
    def depth(self):
        return self.width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return -self.width / 2

    @property
    def right(self):
        return self.width / 2

    @property
    def back(self):
        return -self.width / 2

    @property
    def front(self):
        return self.width / 2

    @property
    def bottom(self):
        return -self.height / 2

    @property
    def top(self):
        return self.height / 2

    def half_down(self):
        return self.down(self.height / 2)

    def half_up(self):
        return self.up(self.height / 2)


class Sphere(Primitive):
    def __init__(self, d, segments=None):
        super().__init__()
        self._diameter = d
        if segments is None:
            segments = int(d * 3.14 / 0.4)
        self._segments = segments

    def _arguments(self):
        return {"d": self._diameter, "$fn": self._segments}

    @property
    def width(self):
        return self._diameter

    @property
    def depth(self):
        return self._diameter

    @property
    def height(self):
        return self._diameter

    @property
    def left(self):
        return -self._diameter / 2

    @property
    def right(self):
        return self._diameter / 2

    @property
    def back(self):
        return -self._diameter / 2

    @property
    def front(self):
        return self._diameter / 2

    @property
    def bottom(self):
        return -self._diameter / 2

    @property
    def top(self):
        return self._diameter / 2


class Polyhedron(Primitive):
    def __init__(self, points, faces, convexity=1):
        super().__init__()
        self.points = list(self.unpack_points(points))
        self.faces = [list(face) for face in faces]
        self.convexity = convexity

    @staticmethod
    def unpack_points(points):
        for point in points:
            if isinstance(point, Point3D):
                yield point
            elif isinstance(point, (tuple, list)) and len(point) == 3:
                x, y, z = point
                yield Point3D(x, y, z)
            else:
                raise ValueError(
                    "invalid point, must be a 3 floats tuple or a Point3D instance",
                    point,
                )

    def _arguments(self):
        return {
            "points": self.points,
            "faces": self.faces,
            "convexity": self.convexity,
        }


# 2D Primitives
class Primitive2D(Primitive):
    @property
    def bottom(self):
        return 0

    @property
    def top(self):
        return 0

    @property
    def height(self):
        return 0


class Circle(Primitive2D):
    def __init__(self, d, segments=None):
        super().__init__()
        self._diameter = d
        if segments is None:
            segments = int(d * 3.14 / 0.4)
        self._segments = segments

    def _arguments(self):
        return {"d": self._diameter, "$fn": self._segments}

    @property
    def left(self):
        return -self._diameter / 2

    @property
    def right(self):
        return self._diameter / 2

    @property
    def back(self):
        return -self._diameter / 2

    @property
    def front(self):
        return self._diameter / 2


class Square(Primitive2D):
    def __init__(self, width: float, depth: float):
        super().__init__()
        self._width = width
        self._depth = depth

    def _arguments(self) -> Dict[Optional[str], Any]:
        return {"size": Point2D(self._width, self._depth), "center": True}

    @property
    def width(self) -> float:
        return self._width

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def left(self) -> float:
        return -self.width / 2

    @property
    def right(self) -> float:
        return self.width / 2

    @property
    def back(self) -> float:
        return -self.depth / 2

    @property
    def front(self) -> float:
        return self.depth / 2


class Text(Primitive2D):
    def __init__(
        self,
        text: str,
        size: int = 10,
        font: str = None,
        halign: str = None,
        valign: str = None,
        spacing: int = None,
        direction: str = None,
        language: str = None,
        script: str = None,
        segments: int = None,
    ):
        super().__init__()
        self.text = text
        self.size = size
        self.font = font
        self.halign = halign
        self.valign = valign
        self.spacing = spacing
        self.direction = direction
        self.language = language
        self.script = script
        self.segments = segments

    def _arguments(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "size": self.size,
            "font": self.font,
            "halign": self.halign,
            "valign": self.valign,
            "spacing": self.spacing,
            "direction": self.direction,
            "language": self.language,
            "script": self.script,
            "$fn": self.segments,
        }

    @property
    def left(self) -> float:
        if self.halign in (None, "left"):
            return 0
        raise NotImplementedError(
            "use halign='left' (default) to be able to align a Text to left"
        )

    @property
    def right(self) -> float:
        if self.halign == "right":
            return 0
        raise NotImplementedError(
            "use halign='right' to be able to align a Text to right"
        )

    @property
    def back(self) -> float:
        if self.valign in (None, "baseline", "bottom"):
            return 0
        raise NotImplementedError(
            "use valign='baseline' or 'bottom' to be able to align a Text to back"
        )

    @property
    def front(self) -> float:
        if self.valign == "top":
            return 0
        raise NotImplementedError(
            "use valign='top' to be able to align a Text to front"
        )


class Polygon(Primitive2D):
    def __init__(
        self,
        *points: typing.Union[Point2D, Tuple[float, float]],
        path: Iterable[int] = None,
        hole_paths: Iterable[Iterable[int]] = None,
        convexity: int = None
    ):
        super().__init__()
        self.points = list(self.unpack_points(points))
        if hole_paths:
            if not path:
                path = list(range(len(points)))
        self.paths: Optional[List[List[int]]] = [list(path)] if path else None
        if hole_paths and self.paths:
            for hole_path in hole_paths:
                self.paths.append(list(hole_path))
        self.convexity = convexity

    @staticmethod
    def unpack_points(
        points: Iterable[typing.Union[Point2D, Tuple[float, float]]]
    ) -> Iterable[Point2D]:
        for point in points:
            if isinstance(point, Point2D):
                yield point
            elif isinstance(point, (tuple, list)) and len(point) == 2:
                x, y = point
                yield Point2D(x, y)
            else:
                raise ValueError(
                    "invalid point, must be a 2 floats tuple or a Point2D instance",
                    point,
                )

    def _arguments(self) -> Dict[str, Any]:
        return {
            "points": self.points,
            "paths": self.paths,
            "convexity": self.convexity,
        }

    @property
    def left(self) -> float:
        return min([point.x for point in self.points])

    @property
    def right(self) -> float:
        return max([point.x for point in self.points])

    @property
    def front(self) -> float:
        return max([point.y for point in self.points])

    @property
    def back(self) -> float:
        return min([point.y for point in self.points])


class Import(Primitive):
    def __init__(self, file, convexity=None, layer=None):
        if not os.path.isabs(file):
            file = os.path.join(os.path.dirname(sys.argv[0]), file)
        super().__init__(file=file, convexity=convexity, layer=layer)


class Echo(Primitive):
    pass
