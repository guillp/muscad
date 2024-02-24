# based on NUT JOB by Mike Mattala: https://www.thingiverse.com/thing:193647
from __future__ import annotations

from math import floor, pi

from muscad import (
    Cylinder,
    Object,
    Part,
    Polygon,
    Polyhedron,
    Tube,
    Union,
    cos,
    sin,
)


class ThreadShape(Part):
    def init(  # type: ignore[override]
        self,
        *,
        length: float,
        outer_diameter: float,
        inner_diameter: float,
        segments: int,
        step: float,
        top_countersink: bool = False,
        bottom_countersink: bool = False,
    ) -> None:
        if not top_countersink and not bottom_countersink:
            self.shape = Tube(height=length, diameter=outer_diameter, bottom=0, segments=segments)
        else:
            self.shape = Tube(bottom=step / 2, height=length - step + 0.005, diameter=outer_diameter, segments=segments)
            self.top_countersink = (
                Tube(
                    bottom=self.shape.top,
                    height=step / 2,
                    diameter=outer_diameter,
                    top_diameter=inner_diameter,
                    segments=segments,
                )
                if top_countersink
                else Tube(bottom=self.shape.top, height=step / 2, diameter=outer_diameter, segments=segments)
            )
            self.bottom_countersink = (
                Tube(
                    height=step / 2,
                    top=self.shape.bottom,
                    diameter=inner_diameter,
                    top_diameter=outer_diameter,
                    segments=segments,
                )
                if bottom_countersink
                else Tube(height=step / 2, top=self.shape.bottom, diameter=outer_diameter, segments=segments)
            )


class ScrewThread(Part):
    def init(  # type: ignore[override]
        self,
        *,
        diameter: float,
        length: float,
        step: int,
        top_countersink: bool = False,
        bottom_countersink: bool = False,
        shape_degrees: float = 45,
        resolution: float = 0.5,
    ) -> None:
        inner_diameter = diameter - step * cos(shape_degrees) / sin(shape_degrees)
        segments = floor(pi * diameter / resolution)
        ttn = round(length / step + 1)
        lfxy = 360 / segments
        zt = step / segments
        self.thread = ThreadShape(
            length=length,
            outer_diameter=diameter,
            inner_diameter=inner_diameter,
            segments=segments,
            step=step,
            top_countersink=top_countersink,
            bottom_countersink=bottom_countersink,
        ) & Union(
            Polyhedron(
                points=[
                    [0, 0, (i - 1) * step],
                    [
                        inner_diameter / 2 * cos(j * lfxy),
                        inner_diameter / 2 * sin(j * lfxy),
                        i * step + j * zt - step,
                    ],
                    [
                        inner_diameter / 2 * cos((j + 1) * lfxy),
                        inner_diameter / 2 * sin((j + 1) * lfxy),
                        i * step + (j + 1) * zt - step,
                    ],
                    [0, 0, i * step],
                    [
                        diameter / 2 * cos(j * lfxy),
                        diameter / 2 * sin(j * lfxy),
                        i * step + j * zt - step / 2,
                    ],
                    [
                        diameter / 2 * cos((j + 1) * lfxy),
                        diameter / 2 * sin((j + 1) * lfxy),
                        i * step + (j + 1) * zt - step / 2,
                    ],
                    [
                        inner_diameter / 2 * cos(j * lfxy),
                        inner_diameter / 2 * sin(j * lfxy),
                        i * step + j * zt,
                    ],
                    [
                        inner_diameter / 2 * cos((j + 1) * lfxy),
                        inner_diameter / 2 * sin((j + 1) * lfxy),
                        i * step + (j + 1) * zt,
                    ],
                    [0, 0, (i + 1) * step],
                ],
                faces=[
                    [1, 0, 3],
                    [1, 3, 6],
                    [6, 3, 8],
                    [1, 6, 4],
                    [0, 1, 2],
                    [1, 4, 2],
                    [2, 4, 5],
                    [5, 4, 6],
                    [5, 6, 7],
                    [7, 6, 8],
                    [7, 8, 3],
                    [0, 2, 3],
                    [3, 2, 7],
                    [7, 2, 5],
                ],
            )
            for i in range(ttn)
            for j in range(segments)
        )


class HexScrew(Part):
    def init(  # type: ignore[override]
        self,
        *,
        thread_outer_diameter: float,
        thread_step: float,
        step_shape_degrees: float,
        thread_length: float,
        resolution: int,
        head_diameter: float,
        head_height: float,
        non_thread_length: float,
        non_thread_diameter: float | None = None,
        countersink: bool = True,
    ) -> None:
        ntd = thread_outer_diameter - thread_step * cos(step_shape_degrees) / sin(step_shape_degrees)
        self.head = HexHead(head_height, head_diameter).align(bottom=0)
        non_thread: Object
        if non_thread_length == 0:
            non_thread = Cylinder(h=0.01, d=ntd)
        else:
            if non_thread_diameter == -1:
                non_thread = Cylinder(h=non_thread_length + 0.01, d=ntd)
            elif non_thread_diameter == 0:
                non_thread = Cylinder(h=non_thread_length - thread_step / 2, d=thread_outer_diameter) + Cylinder(
                    h=thread_step / 2, d=thread_outer_diameter, d2=ntd
                )
            else:
                if non_thread_diameter is None:
                    non_thread_diameter = ntd
                non_thread = Cylinder(h=non_thread_length, d=non_thread_diameter)

        self.non_thread = non_thread.align(bottom=self.head.top)
        self.screw = ScrewThread(
            outer_diameter=thread_outer_diameter,
            step=thread_step,
            shape_degrees=step_shape_degrees,
            length=thread_length,
            resolution=resolution,
            top_countersink=countersink,
            bottom_countersink=False,
        ).align(bottom=self.non_thread.top)


class HexHead(Part):
    def init(self, height: float, diameter: float) -> None:  # type: ignore[override]
        d0 = diameter / sin(60)
        x0 = 0
        x1 = diameter / 2
        x2 = x1 + height / 2
        y0 = 0
        y1 = height / 2
        y2 = height

        self.head = Tube(bottom=0, height=height, d=d0, segments=6) & Polygon(
            (x0, y0), (x1, y0), (x2, y1), (x1, y2), (x0, y2)
        ).z_rotational_extrude(bottom=0)


class HexNut(Part):
    def init(  # type: ignore[override]
        self,
        *,
        diameter: float,
        height: float,
        thread_outer_diameter: float,
        thread_step: float = 2,
        step_shape_degrees: float = 45,
        resolution: float = 0.5,
    ) -> None:
        self.nut = HexHead(height, diameter)
        self.countersinks = ~Tube(
            bottom=self.nut.bottom - 0.1,
            height=thread_step / 2,
            d=thread_outer_diameter,
            d2=thread_outer_diameter - (diameter / 2 + 0.1) * cos(step_shape_degrees) / sin(step_shape_degrees),
        ).z_mirror(center=self.nut.center_z)
        self.bore = ~ScrewThread(
            diameter=thread_outer_diameter, length=height, step=thread_step, shape_degrees=step_shape_degrees
        ).align(center_z=self.nut.center_z)


# HexNut(diameter=9, height=4, thread_outer_diameter=6.2).render_to_file()
