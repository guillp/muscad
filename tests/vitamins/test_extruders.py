from muscad.vitamins.extruders import E3Dv6Extruder

from ..conftest import compare_str


def test_e3dv6() -> None:
    compare_str(
        E3Dv6Extruder(),
        """// extruder
union() {
  translate(v=[0, 0, 0.99])
  cylinder(h=2, d1=1, d2=6, $fn=7, center=true);
  translate(v=[0, 0, 2.98])
  cylinder(h=2, d=8.06, $fn=6, center=true);
  translate(v=[0, 0, 4.97])
  cylinder(h=2, d=5, $fn=39, center=true);
  translate(v=[0, 0, 18.0])
  cylinder(h=3.1, d=4, $fn=31, center=true);
  translate(v=[0, 0, 32.04])
  cylinder(h=25, d=22.3, $fn=175, center=true);
  translate(v=[0, 0, 48.03])
  cylinder(h=7, d=16, $fn=125, center=true);
  translate(v=[0, 0, 54.42])
  cylinder(h=5.8, d=12, $fn=94, center=true);
  translate(v=[0, 0, 60.81])
  cylinder(h=7, d=16, $fn=125, center=true);
  translate(v=[0, 0, 5.96])
  // volume
  translate(v=[0, 5.5, 5.25])
  cube(size=[16, 20.0, 10.5], center=true);
}""",
    )
