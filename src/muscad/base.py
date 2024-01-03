from __future__ import annotations

import math
import os
import subprocess
import typing
from functools import wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    Iterable,
    Literal,
    Protocol,
)

from muscad.helpers import camel_to_snake, normalize_angle


class MuSCAD:
    """Base class for all MuSCAD objects."""

    def render(self) -> str:
        """Returns the SCAD code to render this object.

        :return: the SCAD code for this object.

        """
        raise NotImplementedError()  # pragma: no cover

    def __str__(self) -> str:
        return self.render()

    def _repr_pretty_(self, p: Any, cycle: bool) -> None:  # noqa: FBT001
        """Helper method for Jupyter Notebook to show the rendered code instead of `__repr__`."""
        p.text(str(self))  # pragma: no cover


class MuSCADError(Exception):
    """Base class for all MuSCAD exceptions."""


def indent(s: str, token: str = "  ") -> str:
    r"""Indents a given string, with characters from `token`. Each line will be prefixed by token.

    :param s: the string to indent (may contain multiple lines, separated by '\n'
    :param token: the string to use as indentation
    :return: the indented string

    """
    return token + s.replace("\n", f"\n{token}")


def add_comment(code: str, comment: str | None = None) -> str:
    """Adds comment to a rendered code."""
    if not comment:
        return code
    comment = "".join(f"// {line}\n" for line in comment.split("\n"))
    return f"{comment}{code}"


def render_comment(f: Callable[[O_contra], str]) -> Callable[[O_contra], str]:
    """A helper decorator to add comments to rendered code."""

    @wraps(f)
    def wrapper(self: Any) -> str:
        code = f(self)
        return add_comment(code, self.comment)

    return wrapper


O_contra = typing.TypeVar("O_contra", contravariant=True)


class Object(MuSCAD):
    """Base class for all OpenSCAD geometry objects.

    Do not instantiate this class directly.

    """

    object_name: str

    def __init_subclass__(cls, name: str | None = None):
        """Derive a name from the subclass name, if not explicitly declared.

        :param name: a string (if explicitly declared)
        :param kwargs: remaining attributes (unused)
        :return: a subclass with a `name` attribute

        """
        super().__init_subclass__()
        if name is None:
            cls.object_name = camel_to_snake(cls.__name__)
        else:
            cls.object_name = name

    def __init__(self) -> None:
        """Base constructor for Objects.

        :param children:

        """
        self.modifier: str = ""
        self.comment: str | None = None

    def set_modifier(self, m: str | None) -> Object:
        """Set or remove a modifier for this object.

        :param m: one of OpenSCAD's modifiers, as a single char str, or None to remove the modifier.
        :return: the same object, with modifier applied

        """
        if not m:
            self.modifier = ""
            return self
        self.modifier = m
        return self

    def disable(self) -> Object:
        """Disables the object (modifer *) :return: the same object, disabled."""
        return self.set_modifier("*")

    def debug(self) -> Object:
        """Enables debug for the object (modifier #) :return: the same object, in debug mode."""
        return self.set_modifier("#")

    def background(self) -> Object:
        """Sets the object as background (modifier %) :return: the same object, as background."""
        return self.set_modifier("%")

    def root(self) -> Object:
        """Sets the object as root (modifier !) :return: the same object, as root."""
        return self.set_modifier("!")

    def remove_modifier(self) -> Object:
        """Remove any previously applied modifier.

        :return: the same object, with any modifier removed

        """
        return self.set_modifier(None)

    def __add__(self, other: Object | Iterable[Object]) -> Object:
        """Adding two objects together creates a Union of those objects.

        :param other: another object
        :return: a Union of both objects.

        """
        return Union(self, other)

    def __radd__(self, other: Literal[0]) -> Object:
        """Makes sure sum(*[object, ...]) works.

        :param other: another object, or 0
        :return: a Union of both objects.*

        """
        assert other == 0
        return self

    def __sub__(self, other: Object | Hole | Misc | Iterable[Object]) -> Object:
        """Substracting an object from another creates a Difference of those objects.

        :param other: another object
        :return: a Difference of self - other

        """
        return Difference(self, other)

    def __and__(self, other: Object) -> Object:
        """Logical and between two objects creates an Intersection between those objects.

        :param other: another object
        :return: an Intersection of self and other.

        """
        return Intersection(self, other)

    def translate(self, *, x: float = 0, y: float = 0, z: float = 0) -> Object:
        """Applies a `Translation` to this object.

        :param x: x axis translation
        :param y: y axis translation
        :param z: z axis translation
        :return: a translated object

        """
        if x == y == z == 0:
            return self
        return Translation(x=x, y=y, z=z)(self)

    def x_translate(self, x: float) -> Object:
        return self.translate(x=x)

    def y_translate(self, y: float) -> Object:
        return self.translate(y=y)

    def z_translate(self, z: float) -> Object:
        return self.translate(z=z)

    def rightward(self, dist: float) -> Object:
        """Helper method to apply a Translation to the right on X axis on the current object.

        :param dist: distance in mm
        :return: an object, translated to the right by `dist` mm.

        """
        return self.x_translate(dist)

    def leftward(self, dist: float) -> Object:
        """Helper method to apply a Translation to the left on X axis on the current object.

        :param dist: distance in mm
        :return: an object, translated to the left by `dist` mm.

        """
        return self.x_translate(-dist)

    def forward(self, dist: float) -> Object:
        """Helper method to apply a forward Translation on Y axis on the current object.

        :param dist: distance in mm
        :return: an object, translated forwards by `dist` mm.

        """
        return self.y_translate(dist)

    def backward(self, dist: float) -> Object:
        """Helper method to apply a backward Translation on Y axis on the current object.

        :param dist: distance in mm
        :return: an object, translated backwards by `dist` mm.

        """
        return self.y_translate(-dist)

    def up(self, dist: float) -> Object:
        """Helper method to apply an upwards Translation on Z axis on the current object.

        :param dist: distance in mm
        :return: an object, translated upwards by `dist` mm.

        """
        return self.z_translate(dist)

    def down(self, dist: float) -> Object:
        """Helper method to apply a downwards Translation on Z axis on the current object.

        :param dist: distance in mm
        :return: an object, translated downwards by `dist` mm.

        """
        return self.z_translate(-dist)

    def rotate(
        self,
        *,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        center_z: float = 0,
    ) -> Object:
        """Applies a rotation to this object.

        :param x: x angle
        :param y: y angle
        :param z: z angle
        :param center_x: center of rotation on X axis
        :param center_y: center of rotation on Y axis
        :param center_z: center of rotation on Z axis
        :return: a rotated object

        """
        x = normalize_angle(x)
        y = normalize_angle(y)
        z = normalize_angle(z)
        if x == y == z == 0:
            return self
        if center_x or center_y or center_z:
            return Translation(x=center_x, y=center_y, z=center_z)(
                Rotation(x=x, y=y, z=z)(Translation(x=-center_x, y=-center_y, z=-center_z)(self))
            )
        return Rotation(x=x, y=y, z=z)(self)

    def x_rotate(self, angle: float, center_y: float = 0, center_z: float = 0) -> Object:
        """Helper method to apply a Rotation on X axis on the current object.

        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on X axis.

        """
        return self.rotate(x=angle, center_y=center_y, center_z=center_z)

    def y_rotate(self, angle: float, center_x: float = 0, center_z: float = 0) -> Object:
        """Helper method to apply a Rotation on Y axis on the current object.

        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on Y axis.

        """
        return self.rotate(y=angle, center_x=center_x, center_z=center_z)

    def z_rotate(self, angle: float, center_x: float = 0, center_y: float = 0) -> Object:
        """Helper method to apply a Rotation on Z axis on the current object.

        :param angle: angle in degrees
        :return: an object, rotated by `angle` degrees on Z axis.

        """
        return self.rotate(z=angle, center_x=center_x, center_y=center_y)

    def left_to_right(self) -> Object:
        """Alias for `self.z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.z_rotate(180)

    def left_to_bottom(self) -> Object:
        """Alias for `self.y_rotate(-90).z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.y_rotate(-90).z_rotate(90)

    def left_to_top(self) -> Object:
        """Alias for `self.y_rotate(90).z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.y_rotate(90).z_rotate(90)

    def left_to_front(self) -> Object:
        """Alias for `self.z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(-90)

    def left_to_back(self) -> Object:
        """Alias for `self.z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(90)

    def right_to_bottom(self) -> Object:
        """Alias for `self.y_rotate(90).z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.y_rotate(90).z_rotate(-90)

    def right_to_top(self) -> Object:
        """Alias for `self.y_rotate(-90).z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.y_rotate(-90).z_rotate(90)

    def right_to_front(self) -> Object:
        """Alias for `self.z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(90)

    def right_to_back(self) -> Object:
        """Alias for `self.z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(-90)

    def right_to_left(self) -> Object:
        """Alias for `self.z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.z_rotate(180)

    def front_to_left(self) -> Object:
        """Alias for `self.z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(90)

    def front_to_right(self) -> Object:
        """Alias for `self.z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(-90)

    def front_to_top(self) -> Object:
        """Alias for `self.x_rotate(90).z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(90).z_rotate(180)

    def front_to_bottom(self) -> Object:
        """Alias for `self.x_rotate(-90).z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90).z_rotate(180)

    def front_to_back(self) -> Object:
        """Alias for `self.z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.z_rotate(180)

    def back_to_left(self) -> Object:
        """Alias for `self.z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(-90)

    def back_to_right(self) -> Object:
        """Alias for `self.z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.z_rotate(90)

    def back_to_front(self) -> Object:
        """Alias for `self.z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.z_rotate(180)

    def back_to_top(self) -> Object:
        """Alias for `self.x_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90)

    def back_to_bottom(self) -> Object:
        """Alias for `self.x_rotate(90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(90)

    def bottom_to_left(self) -> Object:
        """Alias for `self.x_rotate(-90).z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90).z_rotate(-90)

    def bottom_to_right(self) -> Object:
        """Alias for `self.x_rotate(-90).z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90).z_rotate(90)

    def bottom_to_front(self) -> Object:
        """Alias for `self.x_rotate(-90).z_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90).z_rotate(180)

    def bottom_to_back(self) -> Object:
        """Alias for `self.x_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90)

    def bottom_to_top(self) -> Object:
        """Alias for `self.x_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(180)

    def top_to_left(self) -> Object:
        """Alias for `self.x_rotate(90).z_rotate(-90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(90).z_rotate(-90)

    def top_to_right(self) -> Object:
        """Alias for `self.x_rotate(90).z_rotate(90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(90).z_rotate(90)

    def top_to_back(self) -> Object:
        """Alias for `self.x_rotate(90)`.

        :return: a rotated Object.

        """
        return self.x_rotate(90)

    def top_to_front(self) -> Object:
        """Alias for `self.x_rotate(-90).y_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(-90).y_rotate(180)

    def top_to_bottom(self) -> Object:
        """Alias for `self.x_rotate(180)`.

        :return: a rotated Object.

        """
        return self.x_rotate(180)

    def upside_down(self, *, x_axis: bool = False) -> Object:
        """Turns the object upside down on its Y axis.

        Equivalent to self.y_rotate(180). If x_axis is True, rotate on X axis instead (like top_to_bottom()).
        :return: an object rotated 180° on X or Y axis

        """
        if x_axis:
            return self.x_rotate(180)
        else:
            return self.y_rotate(180)

    def scale(self, *, x: float = 1.0, y: float = 1.0, z: float = 1.0) -> Object:
        """Applies a scaling transformation to this object.

        :param x: x ratio
        :param y: y ratio
        :param z: z ratio
        :return: a scaled object

        """
        return Scaling(x=x, y=y, z=z)(self)

    def mirror(self, *, x: float = 0, y: float = 0, z: float = 0) -> Object:
        """Applies a mirror transformation to this object.

        :param x: x mirror factor
        :param y: y mirror factor
        :param z: z mirror factor
        :return: a mirrored object

        """
        return Mirroring(x=x, y=y, z=z)(self)

    def x_mirror(self, center: float = 0.0) -> Object:
        """Helper method to mirror this object on the X axis or a parallel.

        :param center: the X coordinate of the axis to mirror on
        :return: a mirrored object

        """
        return self.leftward(center).mirror(x=1).rightward(center)

    def y_mirror(self, center: float = 0.0) -> Object:
        """Helper method to mirror this object on the Y axis or a parallel.

        :param center: the Y coordinate of the axis to mirror on
        :return: a mirrored object

        """
        return self.backward(center).mirror(y=1).forward(center)

    def z_mirror(self, center: float = 0.0) -> Object:
        """Helper method to mirror this object on the Z axis or a parallel.

        :param center: the Y coordinate of the axis to mirror on
        :return: a mirrored object

        """
        return self.down(center).mirror(z=1).up(center)

    def x_symmetry(self, center: float = 0.0) -> Object:
        """Helper method to create a symmetric object using a mirror on a plane parallel to the X plane.

        Similar to x_mirror(), but the original object is kept.

        :param center: the X coordinate of the axis to mirror on
        :return: a symmetric object

        """
        return self.x_mirror(center) + self

    def y_symmetry(self, center: float = 0.0) -> Object:
        """Helper method to create a symmetric object using a mirror on a plane parallel to the Y plane.

        Similar to y_mirror(), but the original object is kept.

        :param center: the Y coordinate of the axis to mirror on
        :return: a symmetric object

        """
        return self.y_mirror(center) + self

    def z_symmetry(self, center: float = 0.0) -> Object:
        """Helper method to create a symmetric object using a mirror on a plane parallel to the Z plane.

        Similar to z_mirror(), but the original object is kept.

        :param center: the Z coordinate of the axis to mirror on
        :return: a symmetric object

        """
        return self.z_mirror(center) + self

    def project(self, *, cut: bool = False) -> Object:
        """Transform this object into a 2D shape by projecting it to the (x,y) plane."""
        return Projection(cut=cut)(self)

    def linear_extrude(
        self,
        height: float,
        *,
        center: bool = False,
        convexity: int = 10,
        twist: float = 0.0,
        slices: int | None = None,
        scale: float = 1.0,
        segments: int | None = None,
    ) -> Object:
        """Applies a linear extrusion transformation to this object.

        :param height: height of the extrusion
        :param center: if true, center the extrusion
        :param convexity:
        :param twist:
        :param slices:
        :param scale:
        :param segments: number of segments. If None, automatically determines the number of segments to get a good-
            looking round result.

        """
        return LinearExtrusion(
            height=height,
            center=center,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        )(self)

    def z_linear_extrude(
        self,
        distance: float | None = None,
        *,
        bottom: float | None = None,
        center_z: float | None = None,
        top: float | None = None,
        convexity: int = 10,
        twist: float = 0.0,
        slices: int | None = None,
        scale: float = 1.0,
        segments: int | None = None,
        downwards: bool = False,
    ) -> Object:
        bottom, center_z, top, distance = calc(bottom, center_z, top, distance)
        extrusion = self.linear_extrude(
            distance,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        )
        if downwards:
            return extrusion.top_to_bottom().align(bottom=bottom)
        return extrusion.align(top=top)

    def y_linear_extrude(
        self,
        distance: float | None = None,
        *,
        back: float | None = None,
        center_y: float | None = None,
        front: float | None = None,
        convexity: int = 10,
        twist: float = 0.0,
        slices: int | None = None,
        scale: float = 1.0,
        segments: int | None = None,
        backwards: bool = False,
    ) -> Object:
        back, center_y, front, distance = calc(back, center_y, front, distance)
        extrusion = self.linear_extrude(
            distance,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        )
        if backwards:
            return extrusion.top_to_back().align(back=back)
        return extrusion.top_to_front().align(front=front)

    def x_linear_extrude(
        self,
        distance: float | None = None,
        *,
        left: float | None = None,
        center_x: float | None = None,
        right: float | None = None,
        convexity: int = 10,
        twist: float = 0.0,
        slices: int | None = None,
        scale: float = 1.0,
        segments: int | None = None,
        leftwards: bool = False,
    ) -> Object:
        left, center_x, right, distance = calc(left, center_x, right, distance)
        extrusion = self.linear_extrude(
            distance,
            convexity=convexity,
            twist=twist,
            slices=slices,
            scale=scale,
            segments=segments,
        )
        if leftwards:
            return extrusion.top_to_left().align(left=left)
        return extrusion.top_to_right().align(right=right)

    def rotational_extrude(
        self,
        angle: float = 360,
        convexity: int | None = None,
        segments: int | None = None,
    ) -> Object:
        """Applies a rotational extrusion to this object.

        :param angle:
        :param convexity:
        :param segments: number of segments. If None, automatically determines the number of segments to get a good-
            looking round result.
        :return:

        """
        return RotationalExtrusion(
            angle=angle,
            convexity=convexity,
            segments=segments,
        )(self)

    def z_rotational_extrude(
        self,
        angle: float | None = None,
        angle_from: float | None = None,
        angle_to: float | None = None,
        radius: float = 0,
        convexity: int | None = None,
        segments: int | None = None,
        center_x: float = 0,
        center_y: float = 0,
        bottom: float | None = None,
        center_z: float | None = None,
        top: float | None = None,
    ) -> Object:
        bottom, center_z, top, _ = calc(from_=bottom, center=center_z, to=top, distance=self.width)
        if angle is None and angle_from is None and angle_to is None:
            angle = 360
            angle_from = 0
        else:
            angle_from, _, angle_to, angle = calc(from_=angle_from, to=angle_to, distance=angle)
        return (
            self.x_translate(radius)
            .rotational_extrude(angle, convexity, segments)
            .z_rotate(angle_from)
            .x_translate(center_x)
            .y_translate(center_y)
            .align(bottom=bottom)
        )

    def hull(self) -> Hull:
        return Hull(self)

    def offset(
        self,
        r: float,
        *,
        delta: float | None = None,
        chamfer: bool = False,
        invert: bool = False,
    ) -> Object:
        if invert:
            if r < 0:
                return self - self.offset(r, delta=delta, chamfer=chamfer)
            else:
                return self.offset(r, delta=delta, chamfer=chamfer) - self
        return Offset(r=r, delta=delta, chamfer=chamfer)(self)

    def color(self, name: str, alpha: float | None = None) -> Object:
        """Applies a color to this object.

        :param name:
        :param alpha:
        :return:

        """
        return Color(name, alpha=alpha)(self)

    def hole(self) -> Hole:
        """Turns this object into a Hole.

        :return: a Hole

        """
        return Hole(self)

    def misc(self) -> Misc:
        """Turns this object into a Misc item.

        :return: a Misc

        """
        return Misc(self)

    def __invert__(self) -> Hole:
        """Operator alternative to .hole().

        :return: a Hole based on this object

        """
        return self.hole()

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def depth(self) -> float:
        return self.front - self.back

    @property
    def height(self) -> float:
        return self.top - self.bottom

    @property
    def left(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def right(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def center_x(self) -> float:
        return (self.right + self.left) / 2

    @property
    def back(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def front(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def center_y(self) -> float:
        return (self.front + self.back) / 2

    @property
    def bottom(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def top(self) -> float:
        raise NotImplementedError()  # pragma: no cover

    @property
    def center_z(self) -> float:
        return (self.top + self.bottom) / 2

    def bounding_box(self) -> Object:
        return Cube(self.width, self.depth, self.height).translate(x=self.left, y=self.back, z=self.bottom)

    def slide(self, *, x: float = 0, y: float = 0, z: float = 0) -> Object:
        return Slide(x=x, y=y, z=z)(self)

    def align(
        self,
        *,
        left: float | None = None,
        center_x: float | None = None,
        right: float | None = None,
        back: float | None = None,
        center_y: float | None = None,
        front: float | None = None,
        bottom: float | None = None,
        center_z: float | None = None,
        top: float | None = None,
    ) -> Object:
        x = y = z = 0.0
        if left is not None:
            x = left - self.left
        elif center_x is not None:
            x = center_x - self.center_x
        elif right is not None:
            x = right - self.right
        if back is not None:
            y = back - self.back
        elif center_y is not None:
            y = center_y - self.center_y
        elif front is not None:
            y = front - self.front
        if bottom is not None:
            z = bottom - self.bottom
        elif center_z is not None:
            z = center_z - self.center_z
        elif top is not None:
            z = top - self.top

        return self.translate(x=x, y=y, z=z)

    def divide(
        self,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        T: float = 0,
    ) -> tuple[Object, Object]:
        """Cut this Object into 2 object, on either a x, or y or z plane."""
        from muscad import Volume

        if x is not None:
            if not self.left < x < self.right:
                msg = (
                    "x must be the x coordinate of a pane that divides the object in 2,"
                    f" between {self.left} and {self.right}"
                )
                raise ValueError(msg)
            return (
                self
                & Volume(
                    left=self.left,
                    right=x - T,
                    back=self.back,
                    front=self.front,
                    bottom=self.bottom,
                    top=self.top,
                ),
                self
                & Volume(
                    left=x + T,
                    right=self.right,
                    back=self.back,
                    front=self.front,
                    bottom=self.bottom,
                    top=self.top,
                ),
            )
        elif y is not None:
            if not self.back < y < self.front:
                msg = (
                    "y must be the y coordinate of a pane that divides the object in 2,"
                    f" between {self.back} and {self.front}"
                )
                raise ValueError(msg)
            return (
                self
                & Volume(
                    left=self.left,
                    right=self.right,
                    back=self.back,
                    front=y - T,
                    bottom=self.bottom,
                    top=self.top,
                ),
                self
                & Volume(
                    left=self.left,
                    right=self.right,
                    back=y + T,
                    front=self.front,
                    bottom=self.bottom,
                    top=self.top,
                ),
            )
        elif z is not None:
            if not self.bottom < z < self.top:
                msg = (
                    "z must be the z coordinate of a pane that divides the object in 2,"
                    f" between {self.bottom} and {self.top}"
                )
                raise ValueError(msg)
            return (
                self
                & Volume(
                    left=self.left,
                    right=self.right,
                    back=self.back,
                    front=self.front,
                    bottom=self.bottom,
                    top=z - T,
                ),
                self
                & Volume(
                    left=self.left,
                    right=self.right,
                    back=self.back,
                    front=self.front,
                    bottom=z + T,
                    top=self.top,
                ),
            )
        else:
            msg = "You must provide one plane to divide the Object, defined by one X, Y, Z coordinate"
            raise ValueError(msg)

    def __stl__(self) -> Object:
        return self  # pragma: no cover

    @property
    def file_name(self) -> str:
        return camel_to_snake(self.__class__.__name__)  # pragma: no cover

    def render_to_file(
        self, path: str | Path | None = None, *, mode: str = "wt", openscad: bool = False
    ) -> Path:  # pragma: no cover
        if path is None:
            path = self.file_name
        return render_to_file(self, path, mode=mode, openscad=openscad)

    def export_stl(self, path: str | Path | None = None) -> Path:  # pragma: no cover
        obj = self.__stl__()
        if path is None:
            path = self.file_name
        scad_path = obj.render_to_file(path=path)
        return export_stl(scad_path)

    def walk(self) -> Iterable[Object]:
        yield self


class Primitive(Object):
    """Base class for simple objects with no children.

    Those are the primitive types such as Cube, Sphere, etc. Do not instantiate this class directly.

    """

    def __init__(self, **kwargs: Any):
        super().__init__()
        self.arguments = kwargs

    def _arguments(self) -> dict[str | None, Any]:
        """Get an argument dict for this object.

        This must be implemented by subclasses
        :return: a dict of arguments as {"param_name": arg_value}

        """
        return self.arguments  # type: ignore[return-value]

    def _iter_arguments(
        self,
    ) -> Iterable[tuple[str | None, str | float]]:
        """Iterates over arguments.

        :return: a iterator of (key, val) tuples

        """
        for key, val in self._arguments().items():
            if val is None:
                continue
            if isinstance(val, str):
                yield key, f'"{val}"'
            elif isinstance(val, float):
                if val == 0.0:
                    yield key, 0
                else:
                    yield key, round(val, 4)
            elif val is True:
                yield key, "true"
            elif val is False:
                yield key, "false"
            elif isinstance(val, (tuple, list)):
                yield key, f"[{', '.join(str(item) for item in val)}]"
            else:
                yield key, val

    @classmethod
    def _render_arguments(cls, params: Iterable[tuple[str | None, Any]]) -> str:
        """Render the parameters for this object as OpenSCAD code.

        (anything between the parenthesis)
        :return: a str

        """
        return ", ".join(f"{key}={val}" if key else f"{val}" for key, val in params)

    @render_comment
    def render(self) -> str:
        """Render this object as OpenSCAD code.

        :return: a str of OpenSCAD code

        """
        return f"{self.modifier}{self.object_name}({self._render_arguments(self._iter_arguments())});"

    def walk(self) -> Iterable[Object]:
        yield self


class Composite(Object):
    """Base class for Boolean operations (Union, Difference, Intersection)."""

    def __init__(self, *children: Object | Iterable[Object]):
        super().__init__()
        self.children: list[Object] = []
        if children:
            self.apply(*children)

    def add_child(self, child: Object | Iterable[Object] | Literal[0]) -> Object:
        """Add a children object to this Composite.

        :param child: the child object to add
        :return: another composite with the additional child

        """
        if child == 0:  # for sum(*Objects)
            return self
        elif isinstance(child, MuSCAD):
            self.children.append(child)
        else:
            self.children.extend(child)
        return self

    def apply(self, *children: Object | Iterable[Object]) -> Object:
        for child in children:
            self.add_child(child)
        return self

    def _iter_children(self) -> Iterable[Object]:
        """Iterate over children :return: an iterable."""
        children = self.children

        # If the only children is a Union, return that union children directly
        if len(children) == 1:
            child = children[0]
            if isinstance(child, Union):
                yield from child._iter_children()
            else:
                yield child
        else:
            for child in children:
                yield child

    @classmethod
    def _render_children(cls, children: Iterable[Object]) -> str:
        """Renders the children of this object as OpenSCAD code (anything between the brackets).

        :return: a str

        """
        return "{" + "".join(f"\n{indent(child.render())}" for child in children) + "\n}"

    @render_comment
    def render(self) -> str:
        """Render this composite as valid OpenSCAD code.

        :return: a str

        """
        return f"{self.modifier}{self.object_name}() " f"{self._render_children(self._iter_children())}"

    def walk(self) -> Iterable[Object]:
        for child in self.children:
            yield from child.walk()


def left(children: Iterable[Object]) -> float:
    return min((child.left for child in children), default=0)


def right(children: Iterable[Object]) -> float:
    return max((child.right for child in children), default=0)


def back(children: Iterable[Object]) -> float:
    return min((child.back for child in children), default=0)


def front(children: Iterable[Object]) -> float:
    return max((child.front for child in children), default=0)


def bottom(children: Iterable[Object]) -> float:
    return min((child.bottom for child in children), default=0)


def top(children: Iterable[Object]) -> float:
    return max((child.top for child in children), default=0)


class Union(Composite):
    """OpenSCAD `union()`."""

    def __add__(self, other: Object | Iterable[Object]) -> Object:
        """Adding to a Union adds a children instead of creating a new Union.

        :param other: a children object
        :return: the same union with children appended.

        """
        return self.add_child(other)

    @property
    def left(self) -> float:
        return left(self.children)

    @property
    def back(self) -> float:
        return back(self.children)

    @property
    def bottom(self) -> float:
        return bottom(self.children)

    @property
    def right(self) -> float:
        return right(self.children)

    @property
    def front(self) -> float:
        return front(self.children)

    @property
    def top(self) -> float:
        return top(self.children)

    def render(self) -> str:
        """If the union has a single child, render it redirectly :return: a str."""
        if len(self.children) == 1:
            return add_comment(self.children[0].render(), self.comment)
        return super().render()


class ImplicitUnion(Union):
    def render(self) -> str:
        return f"{self.modifier}{self._render_children(self._iter_children())}"


class Difference(Composite):
    """OpenSCAD `difference()`."""

    def __sub__(self, other: Object | Misc | Hole | Iterable[Object]) -> Object:
        """Substracting from a Difference adds a children instead of creating a new Difference.

        :param other: a children object
        :return: the same difference with children appended.

        """
        return self.add_child(other)

    @property
    def left(self) -> float:
        return self.children[0].left

    @property
    def right(self) -> float:
        return self.children[0].right

    @property
    def back(self) -> float:
        return self.children[0].back

    @property
    def front(self) -> float:
        return self.children[0].front

    @property
    def bottom(self) -> float:
        return self.children[0].bottom

    @property
    def top(self) -> float:
        return self.children[0].top


class Intersection(Composite):
    """OpenSCAD `intersection()`."""

    def __and__(self, other: Object) -> Object:
        """Intersecting with an Intersection adds a children instead of creating a new Intersection.

        :param other: a children object
        :return: the same intersection with children appended.

        """
        return self.add_child(other)

    @property
    def left(self) -> float:
        return max(child.left for child in self.children)

    @property
    def right(self) -> float:
        return min(child.right for child in self.children)

    @property
    def back(self) -> float:
        return max(child.back for child in self.children)

    @property
    def front(self) -> float:
        return min(child.front for child in self.children)

    @property
    def bottom(self) -> float:
        return max(child.bottom for child in self.children)

    @property
    def top(self) -> float:
        return min(child.top for child in self.children)


class Transformation(Primitive):
    """Base class for transformations.

    MuSCAD Transformations can have 1 single child (which can be a Union of multiple children)

    """

    def __init__(self, *children: Object):
        super().__init__()
        self._child: Object | None = None
        self.apply(*children)

    @property
    def child(self) -> Object:
        if self._child is None:
            msg = "This Transformation has no child"
            raise RuntimeError(msg)
        return self._child

    @child.setter
    def child(self, value: Object) -> None:
        self._child = value

    def _arguments(self) -> dict[str | None, Any]:
        return {}

    def apply(self, *children: Object) -> Object:
        if children:
            if len(children) == 1:
                child = children[0]
                if isinstance(child, Union):
                    self.child = ImplicitUnion(*child.children)
                elif isinstance(child, self.__class__):
                    self.combine(child)
                else:
                    self.child = child
            else:
                self.child = ImplicitUnion(*children)
        return self

    def __call__(self, *children: Object) -> Object:
        return self.apply(*children)

    @render_comment
    def render(self) -> str:
        return f"""\
{self.modifier}{self.object_name}({self._render_arguments(self._iter_arguments())})
{self._render_child()}"""

    def childattr(self, item: str) -> Any:
        """Makes properties from the transformed object accessible through the Transformation.

        :param item: name of an attribute on the child
        :return: the child attribute, with transformation applied

        """
        return self.copy()(getattr(self.child, item))

    def __getattr__(self, item: str) -> Any:
        return self.childattr(item)

    def copy(self) -> Transformation:
        raise NotImplementedError()  # pragma: no cover

    @property
    def file_name(self) -> str:
        return self.child.file_name

    def combine(self, child: Transformation) -> Transformation:
        """When applying multiple transformations of the same type, those may be combined.

        :param child: another Primitive
        :return: an object combining all transformations.

        """
        self.child = child
        return self

    def _render_child(self) -> str:
        return self.child.render()

    @property
    def left(self) -> float:
        if self.child:
            return self.child.left
        return 0

    @property
    def right(self) -> float:
        if self.child:
            return self.child.right
        return 0

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def back(self) -> float:
        if self.child:
            return self.child.back
        return 0

    @property
    def front(self) -> float:
        if self.child:
            return self.child.front
        return 0

    @property
    def depth(self) -> float:
        return self.front - self.back

    @property
    def bottom(self) -> float:
        if self.child:
            return self.child.bottom
        return 0

    @property
    def top(self) -> float:
        if self.child:
            return self.child.top
        return 0

    @property
    def height(self) -> float:
        return self.top - self.bottom

    def walk(self) -> Iterable[Object]:
        for child in self.child.walk():
            yield self.copy()(child)


from .primitives import Cube

# import basic transformations to make sure all helpers work
from .transformations import (
    Color,
    Hull,
    LinearExtrusion,
    Mirroring,
    Offset,
    Projection,
    Rotation,
    RotationalExtrusion,
    Scaling,
    Slide,
    Translation,
)


class Hole(MuSCAD):
    def __init__(self, obj: Object):
        self.object = obj
        super().__init__()

    def __getattr__(self, key: str) -> Any:
        return getattr(self.object, key)

    def __add__(self, other: Object) -> Hole:
        if not isinstance(other, Hole):
            msg = "Holes can only be added to Holes"
            raise TypeError(msg)
        return Hole(self.object + other.object)

    def render(self) -> str:
        return self.object.render()

    @property
    def comment(self) -> str | None:
        return self.object.comment

    @comment.setter
    def comment(self, value: str) -> None:
        self.object.comment = value


class Misc(MuSCAD):
    def __init__(self, obj: Object):
        self.object = obj
        super().__init__()

    def __getattr__(self, key: str) -> Any:
        return getattr(self.object, key)

    def render(self) -> str:
        return self.object.render()

    @property
    def comment(self) -> str | None:
        return self.object.comment

    @comment.setter
    def comment(self, value: str) -> None:
        self.object.comment = value

    def hole(self) -> Hole:
        """Turns this Misc into a Hole."""
        return self.object.hole()

    def __invert__(self) -> Hole:
        """Operator alternative to .hole().

        :return: a Hole based on this object

        """
        return self.object.hole()


def distance_between(one: float, other: float) -> float:
    return abs(one - other)


def middle_of(one: float, other: float) -> float:
    return one + (other - one) / 2


def render_to_file(obj: Object, path: str | Path, *, mode: str, openscad: bool = False) -> Path:
    if not isinstance(path, Path):
        path = Path(path)

    if path.suffix != ".scad":
        path = path.with_suffix(".scad")
    if not path.is_absolute():
        path = Path.cwd() / path

    render = obj.render()
    with path.open(mode) as foutput:
        foutput.write(render)
    if openscad and not os.environ.get("MUSCAD_NO_OPENSCAD"):
        try:
            os.startfile(path)  # type: ignore[attr-defined]
        except AttributeError:
            subprocess.call(["xdg-open", path])

    return path


class Calc(Protocol):
    def __call__(
        self,
        from_: float | None = None,
        center: float | None = None,
        to: float | None = None,
        distance: float | None = None,
    ) -> tuple[float, float, float, float]:
        ...  # pragma: no cover


def validate_calc(
    f: Calc,
) -> Calc:
    def wrapper(
        from_: float | None = None,
        center: float | None = None,
        to: float | None = None,
        distance: float | None = None,
    ) -> tuple[float, float, float, float]:
        _from, _center, _to, _distance = f(from_, center, to, distance)
        if center is not None and _center != center:
            msg = (
                "calculated center incompatible with specified center"
                f" (specified: {center}, calculated: {_center}, difference={center - _center})"
            )
            raise ValueError(msg)
        if distance is not None and not math.isclose(_distance, abs(distance)):
            msg = (
                "calculated distance incompatible with specified from_"
                f" (specified: {distance}, calculated: {_distance}, difference={distance - _distance})"
            )
            raise ValueError(msg)
        if (
            (from_ is not None and to is not None and from_ > to)
            or (from_ is not None and center is not None and from_ > center)
            or (to is not None and center is not None and center > to)
            or (distance is not None and distance < 0)
        ):
            from_, to = to, from_

        if from_ is not None and _from != from_:
            msg = f"calculated from_ incompatible with specified from_ (specified: {from_}, calculated: {_from}, difference={from_ - _from})"
            raise ValueError(msg)
        if to is not None and _to != to:
            msg = f"calculated to incompatible with specified to (specified: {to}, calculated: {_to}, difference={to - _to})"
            raise ValueError(msg)
        return _from, _center, _to, _distance

    return wrapper


@validate_calc
def calc(
    from_: float | None = None,
    center: float | None = None,
    to: float | None = None,
    distance: float | None = None,
) -> tuple[float, float, float, float]:
    """Given at least 2 of from_, center, and distance, returns all 4.

    If only distance is given, default to center = 0

    """
    if distance is not None and from_ is None and to is None and center is None:
        center = 0

    if from_ is not None and center is not None:
        if from_ < center:
            distance = (center - from_) * 2
            to = from_ + distance
            return from_, center, to, distance
        else:
            distance = (from_ - center) * 2
            to = from_ - distance
            return to, center, from_, distance
    if from_ is not None and to is not None:
        if from_ < to:
            distance = to - from_
            center = from_ + distance / 2
            return from_, center, to, distance
        else:
            distance = from_ - to
            center = to + distance / 2
            return to, center, from_, distance
    if from_ is not None and distance is not None:
        to = from_ + distance
        distance = abs(distance)
        if from_ < to:
            center = from_ + distance / 2
            return from_, center, to, distance
        else:
            center = to + distance / 2
            return to, center, from_, distance
    if center is not None and to is not None:
        if center < to:
            distance = (to - center) * 2
            from_ = to - distance
            return from_, center, to, distance
        else:
            distance = (center - to) * 2
            from_ = to + distance
            return to, center, from_, distance
    if center is not None and distance is not None:
        distance = abs(distance)
        from_ = center - distance / 2
        to = center + distance / 2
        return from_, center, to, distance
    if to is not None and distance is not None:
        from_ = to - distance
        distance = abs(distance)
        if from_ < to:
            center = (to - from_) / 2 + from_
            return from_, center, to, distance
        else:
            center = (from_ - to) / 2 + from_
            return to, center, from_, distance
    msg = "no sufficient input to calculate all params"
    raise ValueError(msg)


def export_stl(scad_path: str | Path, stl_path: str | Path | None = None) -> Path:
    if stl_path is None:
        stl_path = Path(scad_path).stem + ".stl"
    if not isinstance(stl_path, Path):
        stl_path = Path(stl_path)
    subprocess.call(["openscad", "-o", stl_path, scad_path])
    return stl_path


E = 0.02  # an EPSILON value. Use it when you want to make sure that 2 aligned planes do not overlap
EE = 0.04  # a double EPSILON value.
EEE = 0.06  # triple EPSILON value.

T = 0.1  # a small TOLERANCE value.
TT = 0.2  # a large TOLERANCE value.
TTT = 0.3  # a very large TOLERANCE value

INFINITY = 999_999_999  # a seemingly infinite length
