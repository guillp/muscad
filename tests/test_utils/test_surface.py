"""Tests for the Surface helper class."""

from muscad import Circle, Square, Surface, Union
from tests.utils import compare_str


def test_heart_z() -> None:
    """Creates a 3D Heart, extruded along Z axis."""
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_symmetry()
        .z_linear_extrude(bottom=-1, top=3)
    )

    assert compare_str(
        heart,
        """translate(v=[0, 0, -1.0])
linear_extrude(height=4, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
}""",
    )


def test_spade_z() -> None:
    """Creates a 3D Spade, extruded along Z axis."""
    spade = (
        (
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            )
            + Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            )
        )
        .x_symmetry()
        .z_linear_extrude(bottom=-1, top=4)
    )

    assert compare_str(
        spade,
        """translate(v=[0, 0, -1.0])
linear_extrude(height=5, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
}""",
    )


def test_heart_y() -> None:
    """Creates a 3D Heart, extruded along Y axis."""
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_symmetry()
        .y_linear_extrude(back=3, front=6)
    )

    assert compare_str(
        heart,
        """translate(v=[0, 3.0, 0])
rotate(a=[270, 180, 0])
linear_extrude(height=3, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
}""",
    )


def test_spade_y() -> None:
    """Creates a 3D Spade, extruded along Y axis."""
    spade = (
        Union(
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            ),
            Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            ),
        )
        .x_symmetry()
        .y_linear_extrude(10, center_y=3)
    )

    assert compare_str(
        spade,
        """translate(v=[0, -2.0, 0])
rotate(a=[270, 180, 0])
linear_extrude(height=10, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
}""",
    )


def test_heart_x() -> None:
    """Creates a 3D Heart, extruded along X axis."""
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_symmetry()
        .x_linear_extrude(5, leftwards=True)
    )

    assert compare_str(
        heart,
        """translate(v=[2.5, 0, 0])
rotate(a=[90, 0, 270])
linear_extrude(height=5, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
  hull()
  {
    translate(v=[-7.0, 20.0, 0])
    circle(d=20, $fn=157);
    translate(v=[0, 1.0, 0])
    circle(d=2, $fn=15);
  }
}""",
    )


def test_spade_x() -> None:
    """Creates a 3D Spade, extruded along X axis."""
    spade = (
        (
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            )
            + Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            )
        )
        .x_symmetry()
        .x_linear_extrude(9, left=-3)
    )

    assert compare_str(
        spade,
        """translate(v=[-3.0, 0, 0])
rotate(a=[90, 0, 90])
linear_extrude(height=9, center=false, convexity=10, twist=0, scale=1.0)
{
  mirror(v=[1, 0, 0])
  {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull()
    {
      translate(v=[-10.0, 15.0, 0])
      circle(d=20, $fn=157);
      translate(v=[0, 34.0, 0])
      circle(d=2, $fn=15);
    }
    hull()
    {
      translate(v=[4.0, 1.0, 0])
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0])
      square(size=[1, 15], center=true);
    }
  }
}""",
    )


def test_triangle_in_circle() -> None:
    """Test for Surface.triangle_in_circle()."""
    triangle = Surface.triangle_in_circle(10)
    assert compare_str(
        triangle,
        "polygon(points=[[-8.6603, -5.0], [0, 10], [8.6603, -5.0]], paths=[[0, 1, 2]]);",
    )


def test_regular_polygon() -> None:
    """Test for Surface.regular_polygon()."""
    octogon = Surface.regular_polygon(8, 10)
    assert compare_str(
        octogon,
        "polygon(points=[[10.0, 0], [7.0711, 7.0711], [0.0, 10.0], [-7.0711, 7.0711], [-10.0, 0.0], [-7.0711, -7.0711], [-0.0, -10.0], [7.0711, -7.0711]]);",
    )

    pentagon = Surface.regular_polygon(5, 10)
    assert compare_str(
        pentagon,
        "polygon(points=[[10.0, 0], [3.0902, 9.5106], [-8.0902, 5.8779], [-8.0902, -5.8779], [3.0902, -9.5106]]);",
    )
