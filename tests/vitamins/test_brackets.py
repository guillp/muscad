from muscad.vitamins.brackets import CastBracket

from ..utils import compare_str


def test_castbracket3030() -> None:
    compare_str(
        CastBracket.bracket3030(),
        """difference() {
  // body
  // volume
  cube(size=[36.0, 36.0, 28.0], center=true);
  // clearance
  translate(v=[18.0, 18.0, 0])
  rotate(a=[0, 0, 45])
  // volume
  cube(size=[45.0, 45.0, 28.04], center=true);
}""",
    )
