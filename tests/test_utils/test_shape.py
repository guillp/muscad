"""Tests for the Shape helper class."""
from muscad import Shape
from tests.conftest import compare_str


def test_pipe() -> None:
    """Test for Shape.pipe()."""
    pipe = Shape.pipe(40, 10, 8)
    assert compare_str(
        pipe,
        """difference() {
  cylinder(h=40, d=10, $fn=78, center=true);
  cylinder(h=40.04, d=8, $fn=62, center=true);
}""",
    )


def test_cone() -> None:
    """Test for Shape.cone()."""
    cone = Shape.cone(10, 10)
    assert compare_str(cone, """cylinder(h=10, d1=10, d2=0, $fn=78, center=true);""")


def test_oval_prism() -> None:
    """Test for Shape.oval_prism()."""
    oval_prism = Shape.oval_prism(10, 5, 7)
    assert compare_str(
        oval_prism,
        """scale(v=[1.0, 0.7143, 1.0])
cylinder(h=10, d=7, $fn=54, center=true);""",
    )


def test_oval_tube() -> None:
    """Test for Shape.oval_tube()."""
    oval_tube = Shape.oval_tube(height=10, x_diameter=20, y_diameter=10, wall=1)
    assert compare_str(
        oval_tube,
        """difference() {
  scale(v=[1.0, 0.5, 1.0])
  cylinder(h=10, d=20, $fn=157, center=true);
  scale(v=[0.9, 0.4, 1.0])
  cylinder(h=10.04, d=20, $fn=157, center=true);
}""",
    )
