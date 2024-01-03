from __future__ import annotations

from contextlib import suppress

from muscad import Cylinder, Part, calc


class Barrel(Part):
    def init(  # type: ignore[override]
        self,
        d: float | None = None,
        *,
        r: float | None = None,
        d2: float | None = None,
        r2: float | None = None,
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
    ) -> None:
        match d, r:
            case None, None:
                # no explicit diameter or radius, try to deduce it from the other params
                with suppress(ValueError):
                    left, center_x, right, width = calc(left, center_x, right, width)
                with suppress(ValueError):
                    back, center_y, front, depth = calc(back, center_y, front)
                match width, depth:
                    case None, None:
                        msg = (
                            "No sufficient parameter to calculate the barrel diameter."
                            " Please provide either a diameter `d`, a radius `r`,"
                            "or at least 2 two parameters on axis X or Y."
                        )
                        raise ValueError(msg)
                    case float(), None:
                        d = width
                    case None, float():
                        d = depth
                    case float(), float() if width != depth:
                        msg = (
                            f"width ({width}mm) is different from depth ({depth}mm)."
                            " I don't know which one to use as diameter."
                        )
                        raise ValueError(msg)
            case float(), None:
                pass
            case None, float() if r is not None:
                d = r * 2
            case float(), float() if r is not None and d is not None and r * 2 != d:
                msg = (
                    "diameter `d` and radius `r` must be consistent." "Please fix, or provide either one or the other."
                )
                raise ValueError(msg)

        assert d is not None

        match r2, d2:
            case None, float():
                pass
            case float(), None if r2 is not None:
                d2 = r2 * 2
            case float(), float() if d2 is not None and r2 is not None and d2 != r2 * 2:
                msg = (
                    f"inconsistent top diameter `d2` ({d2}mm) and top radius ({r2}mm)."
                    "Please fix, or provide either one or the other."
                )
                raise ValueError(msg)

        match width, d:
            case None, float():
                width = d
            case float(), float() if width != d:
                msg = f"diameter `d` ({d}mm) is different from width ({width}mm)."
                raise ValueError(msg)

        match depth, d:
            case None, float():
                depth = d
            case float(), None:
                assert False
            case float(), float() if depth != d:
                msg = f"diameter `d` ({d}mm) is different from depth ({depth}mm)."
                raise ValueError(msg)

        self._left, self._center_x, self._right, self._width = calc(left, center_x, right, width)
        self._back, self._center_y, self._front, self._depth = calc(back, center_y, front, depth)
        self._bottom, self._center_z, self._top, self._height = calc(bottom, center_z, top, height)
        self.cylinder = Cylinder(d=d, d2=d2, h=self._height, segments=segments).align(
            center_x=self._center_x, center_y=self._center_y, center_z=self._center_z
        )

    @property
    def left(self) -> float:
        return self._left

    @property
    def right(self) -> float:
        return self._right

    @property
    def back(self) -> float:
        return self._back

    @property
    def front(self) -> float:
        return self._front

    @property
    def bottom(self) -> float:
        return self._bottom

    @property
    def top(self) -> float:
        return self._top
