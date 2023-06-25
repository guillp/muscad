"""Tests for muscad.vitamins.cable_chain."""
from muscad.vitamins.cable_chain import CableChain
from tests.conftest import compare_str


def test_cable_chain() -> None:
    female, male = CableChain.couple(16, 6)
    assert compare_str(
        female,
        """difference() {
  // cylinder
  translate(v=[0, 0, 0.5])
  cylinder(h=0.6, d=15.8, $fn=124, center=true);
  // tunnel_hole
  translate(v=[0, 0, 0.5])
  cylinder(h=2.6, d=6.2, $fn=48, center=true);
}""",
    )
    assert compare_str(
        male,
        """difference() {
  // cylinder
  translate(v=[0, 0, 1.0])
  cylinder(h=2.0, d=15.8, $fn=124, center=true);
  // clearance
  difference() {
    // cylinder
    translate(v=[0, 0, 2.0])
    cylinder(h=0.4, d=16.2, $fn=127, center=true);
    // tunnel_hole
    translate(v=[0, 0, 2.0])
    cylinder(h=2.4, d=5.6, $fn=43, center=true);
  }
}""",
    )
