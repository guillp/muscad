from ..conftest import compare_str
from muscad.vitamins.pulleys import Pulley


def test_pulley():
    compare_str(
        Pulley.GT2(16),
        """union() {
  // body
  cylinder(h=6, d=9.6779, $fn=75, center=true);
  // shaft
  cylinder(h=20, d=3.4, $fn=26, center=true);
}""",
    )
