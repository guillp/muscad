"""Tests for muscad.vitamins.bearings"""
from tests.conftest import compare_str

from muscad.vitamins.bearings import BushingLinearBearing


def test_bushing():
    BushingLinearBearing.SC8UU()

    test = BushingLinearBearing.SC8UU()
    assert compare_str(
        test,
        """union() {
  // base
  // volume
  cube(size=[34.4, 30.4, 22.4], center=true);
  // bolts
  union() {
    translate(v=[-12.0, -9.0, -9.82])
    union() {
      // thread
      cylinder(h=10, d=4.378, $fn=34, center=true);
      // head
      translate(v=[0, 0, -7.08])
      cylinder(h=4.2, d=7.3, $fn=57, center=true);
    }
    translate(v=[-12.0, 9.0, -9.82])
    union() {
      // thread
      cylinder(h=10, d=4.378, $fn=34, center=true);
      // head
      translate(v=[0, 0, -7.08])
      cylinder(h=4.2, d=7.3, $fn=57, center=true);
    }
    translate(v=[12.0, -9.0, -9.82])
    union() {
      // thread
      cylinder(h=10, d=4.378, $fn=34, center=true);
      // head
      translate(v=[0, 0, -7.08])
      cylinder(h=4.2, d=7.3, $fn=57, center=true);
    }
    translate(v=[12.0, 9.0, -9.82])
    union() {
      // thread
      cylinder(h=10, d=4.378, $fn=34, center=true);
      // head
      translate(v=[0, 0, -7.08])
      cylinder(h=4.2, d=7.3, $fn=57, center=true);
    }
  }
}""",
    )
