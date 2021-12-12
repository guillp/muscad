"""Tests for the Part class."""
from tests.conftest import compare_str

from muscad import Cube
from muscad import MirroredPart
from muscad import Part


def test_part() -> None:
    """Basic tests for a Part.

    Checks that a Part contain a single child has the same bounding box as this child.
    """
    cube = Cube(8, 10, 12)
    part = Part()
    part.add_child(cube)

    assert part.left == cube.left
    assert part.right == cube.right
    assert part.back == cube.back
    assert part.front == cube.front
    assert part.bottom == cube.bottom
    assert part.top == cube.top

    assert compare_str(part, "cube(size=[8, 10, 12], center=true);")


def test_mirrored_part() -> None:
    """Tests for MirroredPart."""

    class TestMirroredPart(MirroredPart, x=True, keep_x=True):
        cube = Cube(8, 10, 12).align(left=0, back=0, bottom=0)

    part = TestMirroredPart()

    assert part.left == -8
    assert part.right == 8
    assert part.back == 0
    assert part.front == 10
    assert part.bottom == 0
    assert part.top == 12

    assert compare_str(
        part,
        """union() {
  mirror(v=[1, 0, 0])
  {
  // cube
  translate(v=[4.0, 5.0, 6.0])
  cube(size=[8, 10, 12], center=true);
  }
  // cube
  translate(v=[4.0, 5.0, 6.0])
  cube(size=[8, 10, 12], center=true);
}""",
    )
