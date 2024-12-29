"""Tests for Fillet and Chamfer."""

from muscad import Chamfer
from tests.utils import compare_str


def test_chamfer_default_angle() -> None:
    """Tests a Chamfer at the default 45° angle."""
    chamfer = Chamfer(4)
    compare_str(
        chamfer,
        """difference() {
  // box
  translate(v=[2.0, 2.0, 0])
  square(size=[4.04, 4.04], center=true);
  // chamfer
  rotate(a=[0, 0, 45])
  square(size=[5.6569, 6.6569], center=true);
}""",
    )


def test_chamfer_custom_angle() -> None:
    """Tests a Chamfer at custom 30° angle."""
    chamfer = Chamfer(5, 30)
    print(chamfer)
