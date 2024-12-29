from muscad.vitamins.boards import Board
from muscad.vitamins.bolts import Bolt

from ..utils import compare_str


def test_raspberry_pi_3b() -> None:
    compare_str(
        Board.raspberry_pi_3b(bolt=Bolt.M3(10)),
        """union() {
  // board
  // volume
  cube(size=[85.0, 56.0, 2.0], center=true);
  // components
  // volume
  translate(v=[0, 0, 11.0])
  cube(size=[85.0, 56.0, 20.0], center=true);
  // bolts
  union() {
    translate(v=[-39.0, -24.5, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
    }
    translate(v=[-39.0, 24.5, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
    }
    translate(v=[19.0, 24.5, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
    }
    translate(v=[19.0, -24.5, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
    }
  }
}""",
    )
