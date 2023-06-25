from muscad import Cylinder, Part, T
from muscad.utils.stack import stack
from muscad.utils.volume import Volume


class E3Dv6Extruder(Part):
    extruder = stack(
        Cylinder(d=1, d2=6, h=2),
        Cylinder(d=8.06, h=2, segments=6),
        Cylinder(d=5, h=2),
        Volume(left=-8, width=16, back=-4.5, depth=20, bottom=0, height=10.5).misc(),
        Cylinder(d=4, h=3.1),
        Cylinder(d=22.3, h=25),
        Cylinder(d=16, h=7),
        Cylinder(d=12, h=6 - 2 * T),
        Cylinder(d=16, h=7),
    )
