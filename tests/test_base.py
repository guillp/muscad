"""Tests for all MuSCAD primitives."""
import pytest
from tests.conftest import compare_str

from muscad import calc
from muscad import Circle
from muscad import Cube
from muscad import E
from muscad import Echo
from muscad import Sphere
from muscad import Square
from muscad import Text
from muscad import Union


def test_calc():
    # calc() returns (from, center, to, distance)
    assert calc(from_=0, to=10) == (0, 5, 10, 10)
    assert calc(from_=0, center=5) == (0, 5, 10, 10)
    assert calc(from_=0, distance=10) == (0, 5, 10, 10)
    assert calc(distance=10) == (-5, 0, 5, 10)
    assert calc(center=5, to=10) == (0, 5, 10, 10)
    assert calc(center=5, distance=10) == (0, 5, 10, 10)

    assert calc(from_=0, center=5, to=10, distance=10) == (0, 5, 10, 10)
    assert calc(from_=0, center=5, to=10) == (0, 5, 10, 10)
    assert calc(center=5, to=10, distance=10) == (0, 5, 10, 10)
    assert calc(from_=0, to=10, distance=10) == (0, 5, 10, 10)
    assert calc(from_=0, center=5, distance=10) == (0, 5, 10, 10)

    with pytest.raises(ValueError):
        calc()

    calc(from_=0, center=4, to=10, distance=10)


def test_cube() -> None:
    """Test for Cube."""
    cube = Cube(50, 50, 50)
    cube -= Text("top", halign="center", valign="center").z_linear_extrude(
        1, top=cube.top + E
    )
    cube -= Text("bottom", halign="center", valign="center").z_linear_extrude(
        1, bottom=cube.bottom - E, downwards=True
    )
    cube -= Text("right", halign="center", valign="center").x_linear_extrude(
        1, right=cube.right + E
    )
    cube -= Text("left", halign="center", valign="center").x_linear_extrude(
        1, left=cube.left - E, leftwards=True
    )
    cube -= Text("front", halign="center", valign="center").y_linear_extrude(
        1, front=cube.front + E
    )
    cube -= Text("back", halign="center", valign="center").y_linear_extrude(
        1, back=cube.back - E, backwards=True
    )

    assert compare_str(
        cube,
        """difference() {
  cube(size=[50, 50, 50], center=true);
  translate(v=[0, 0, 24.02])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="top", size=10, halign="center", valign="center");
  translate(v=[0, 0, -24.02])
  rotate(a=[180, 0, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="bottom", size=10, halign="center", valign="center");
  translate(v=[24.02, 0, 0])
  rotate(a=[90, 0, 90])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="right", size=10, halign="center", valign="center");
  translate(v=[-24.02, 0, 0])
  rotate(a=[90, 0, 270])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="left", size=10, halign="center", valign="center");
  translate(v=[0, 24.02, 0])
  rotate(a=[270, 180, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="front", size=10, halign="center", valign="center");
  translate(v=[0, -24.02, 0])
  rotate(a=[90, 0, 0])
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  text(text="back", size=10, halign="center", valign="center");
}""",
    )


def test_modifiers() -> None:
    """Test for Object modifiers root(), disable(), debug() and background()."""
    ref = Square(1, 1)
    rendered = ref.render()
    assert ref.root().render() == f"!{rendered}"
    assert ref.disable().render() == f"*{rendered}"
    assert ref.debug().render() == f"#{rendered}"
    assert ref.background().render() == f"%{rendered}"
    assert ref.background().remove_modifier().render() == rendered


def test_sum() -> None:
    """Test for sum() that creates Unions."""
    assert compare_str(
        sum(Cube(1, 1, x) for x in range(2)),
        """union() {
  cube(size=[1, 1, 0], center=true);
  cube(size=[1, 1, 1], center=true);
}""",
    )


def test_translate() -> None:
    """Test for Object.translate() and helper aliases."""
    sphere1 = Sphere(d=10, segments=8).translate(x=4, y=-3, z=5)
    sphere2 = Sphere(d=10, segments=8).up(5).rightward(4).backward(3)

    assert sphere1.render() == sphere2.render()
    assert compare_str(
        sphere1,
        """translate(v=[4, -3, 5])
        sphere(d=10, $fn=8);""",
    )
    assert compare_str(
        sphere2,
        """translate(v=[4, -3, 5])
sphere(d=10, $fn=8);""",
    )


def test_rotational_extrusion() -> None:
    """Test for Object.rotational_extrude()."""
    buoy = Circle(d=10).align(center_x=10).rotational_extrude()
    assert compare_str(
        buoy,
        """rotate_extrude(angle=360, $fn=45)
translate(v=[10.0, 0, 0])
circle(d=10, $fn=78);""",
    )


def test_mirror() -> None:
    """Test for Object.?_mirror()."""
    x_mirrored_circle = Circle(d=10).align(left=0).x_mirror()
    assert x_mirrored_circle.left == -10
    assert x_mirrored_circle.right == 0

    y_mirrored_circle = Circle(d=10).align(back=0).y_mirror()
    assert y_mirrored_circle.back == -10
    assert y_mirrored_circle.front == 0

    z_mirrored_circle = Sphere(d=10).align(bottom=0).z_mirror()
    assert z_mirrored_circle.bottom == -10
    assert z_mirrored_circle.top == 0
    assert z_mirrored_circle.left == -5
    assert z_mirrored_circle.right == 5

    x_mirrored_circle = Circle(d=10).align(left=0).x_mirror(keep=True)
    assert x_mirrored_circle.left == -10
    assert x_mirrored_circle.right == 10

    y_mirrored_circle = Circle(d=10).align(back=0).y_mirror(keep=True)
    assert y_mirrored_circle.back == -10
    assert y_mirrored_circle.front == 10

    z_mirrored_circle = Sphere(d=10).align(bottom=0).z_mirror(keep=True)
    assert z_mirrored_circle.bottom == -10
    assert z_mirrored_circle.top == 10


def test_hull() -> None:
    """Test for Hull."""
    hulled_mirrored_circle = Circle(d=10).align(left=0).x_mirror(keep=True).hull()
    assert compare_str(
        hulled_mirrored_circle,
        """hull()
{
  mirror(v=[1, 0, 0])
  translate(v=[5.0, 0, 0])
  circle(d=10, $fn=78);
  translate(v=[5.0, 0, 0])
  circle(d=10, $fn=78);
}""",
    )

    assert compare_str(
        hulled_mirrored_circle.bounding_box(),
        """translate(v=[-10.0, -5.0, 0])
cube(size=[20.0, 10.0, 0], center=true);""",
    )


def test_echo() -> None:
    """Test for Echo."""
    echo = Echo(foo="bar")
    assert compare_str(echo, 'echo(foo="bar");')


def test_inner_union() -> None:
    """Makes sure that multiple stacked Unions are no-op."""
    union = Union(Union(Union(Circle(d=4))))
    assert compare_str(union, "circle(d=4, $fn=31);")


def test_intersection() -> None:
    """Test for & operator (which creates an Intersection)."""
    intersect = Cube(10, 8, 6) & Cube(6, 8, 10) & Cube(6, 10, 8)
    assert intersect.left == -3
    assert intersect.right == 3
    assert intersect.center_x == 0
    assert intersect.back == -4
    assert intersect.front == 4
    assert intersect.center_y == 0
    assert intersect.bottom == -3
    assert intersect.top == 3
    assert intersect.center_z == 0


def test_calc() -> None:
    """Test for the calc() function."""
    from_, center, to, distance = calc(from_=0, center=5, to=10, distance=10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=0, center=5)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=5, center=0)
    assert from_ == -5
    assert center == 0
    assert to == 5
    assert distance == 10

    from_, center, to, distance = calc(from_=5, distance=10)
    assert from_ == 5
    assert center == 10
    assert to == 15
    assert distance == 10

    from_, center, to, distance = calc(center=5, to=10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(center=10, to=5)
    assert from_ == 5
    assert center == 10
    assert to == 15
    assert distance == 10

    from_, center, to, distance = calc(from_=10, distance=-10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=10, to=-10)
    assert from_ == -10
    assert center == 0
    assert to == 10
    assert distance == 20

    with pytest.raises(ValueError):
        calc(from_=5, center=0, to=-8)

    with pytest.raises(ValueError):
        calc(from_=0, center=4, to=10, distance=10)


def test_color() -> None:
    """Test for Object.color()."""
    colored_cube = Cube(10, 10, 10).color("blue")
    assert compare_str(
        colored_cube,
        """color("blue")
cube(size=[10, 10, 10], center=true);""",
    )


def test_rotation() -> None:
    """Test for Object.rotate()."""
    cube = Cube(10, 8, 6)

    assert cube.rotate(x=90, z=25, center_y=10)
