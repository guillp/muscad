from muscad import Color
from muscad import Cube
from muscad import Cylinder
from muscad import Hull
from muscad import LinearExtrusion
from muscad import Minkowski
from muscad import Multmatrix
from muscad import Offset
from muscad import Projection
from muscad import Rotation
from muscad import RotationalExtrusion
from muscad import Scaling
from muscad import Slide
from muscad import Square
from muscad import Translation


def test_translation():
    t = Translation(x=1, y=2, z=3)(Cube(2, 2, 2))
    assert (
        t.render() == """translate(v=[1, 2, 3]) \ncube(size=[2, 2, 2], center=true);"""
    )
    assert t.left == 0
    assert t.right == 2
    assert t.center_x == 1
    assert t.back == 1
    assert t.front == 3
    assert t.center_y == 2
    assert t.bottom == 2
    assert t.top == 4
    assert t.center_z == 3


def test_rotation():
    r = Rotation(x=90, y=180, z=-90)(Cube(2, 5, 7))
    assert (
        r.render()
        == """rotate(a=[90, 180, 270]) \ncube(size=[2, 5, 7], center=true);"""
    )
    assert r.left == -3.5
    assert r.right == 3.5
    assert r.center_x == 0
    assert r.back == -1
    assert r.front == 1
    assert r.center_y == 0
    assert r.bottom == -2.5
    assert r.top == 2.5
    assert r.center_z == 0


def test_scaling():
    s = Scaling(x=2, y=3, z=4)(Cube(2, 5, 7))
    assert s.render() == """scale(v=[2, 3, 4]) \ncube(size=[2, 5, 7], center=true);"""
    assert s.left == -2
    assert s.right == 2
    assert s.center_x == 0
    assert s.back == -7.5
    assert s.front == 7.5
    assert s.center_y == 0
    assert s.bottom == -14
    assert s.top == 14
    assert s.center_z == 0


def test_color():
    c = Color("blue")(Cube(2, 5, 7))
    assert c.render() == """color("blue") \ncube(size=[2, 5, 7], center=true);"""
    assert c.left == -1
    assert c.right == 1
    assert c.center_x == 0
    assert c.back == -2.5
    assert c.front == 2.5
    assert c.center_y == 0
    assert c.bottom == -3.5
    assert c.top == 3.5
    assert c.center_z == 0


def test_offset():
    o = Offset(r=1)(Cube(2, 5, 7))
    assert (
        o.render()
        == """offset(r=1, chamfer=false) \ncube(size=[2, 5, 7], center=true);"""
    )


def test_minkowski():
    m = Minkowski(Cube(2, 5, 7), Cylinder(h=7, d=2))
    assert (
        m.render()
        == "minkowski() \n{\n  cube(size=[2, 5, 7], center=true);\n  cylinder(h=7, d=2, $fn=15, center=true);\n}"
    )
    assert m.left == -2
    assert m.right == 2
    assert m.center_x == 0
    assert m.back == -3.5
    assert m.front == 3.5
    assert m.center_y == 0
    assert m.bottom == -3.5
    assert m.top == 3.5
    assert m.center_z == 0


def test_hull():
    h = Hull(Cube(2, 5, 7), Cylinder(h=4, d=4))
    assert (
        h.render()
        == "hull() \n{\n  cube(size=[2, 5, 7], center=true);\n  cylinder(h=4, d=4, $fn=31, center=true);\n}"
    )
    assert h.left == -2
    assert h.right == 2
    assert h.center_x == 0
    assert h.back == -2.5
    assert h.front == 2.5
    assert h.center_y == 0
    assert h.bottom == -3.5
    assert h.top == 3.5
    assert h.center_z == 0


def test_projection():
    p = Projection()(Cube(2, 5, 7))
    assert p.render() == "projection(cut=false) \ncube(size=[2, 5, 7], center=true);"
    assert p.left == -1
    assert p.right == 1
    assert p.center_x == 0
    assert p.back == -2.5
    assert p.front == 2.5
    assert p.center_y == 0
    assert p.bottom == 0
    assert p.top == 0
    assert p.center_z == 0


def test_linear_extrusion():
    le = LinearExtrusion(5)(Square(8, 6))
    assert (
        le.render()
        == "linear_extrude(height=5, center=false, convexity=10, twist=0, scale=1.0) \nsquare(size=[8, 6], center=true);"
    )
    assert le.left == -4
    assert le.right == 4
    assert le.center_x == 0
    assert le.back == -3
    assert le.front == 3
    assert le.center_y == 0
    assert le.bottom == 0
    assert le.top == 5
    assert le.center_z == 2.5


def test_rotational_extrusion():
    re = RotationalExtrusion()(Square(8, 6).align(left=0, back=0))
    assert (
        re.render()
        == "rotate_extrude(angle=360, $fn=45) \ntranslate(v=[4.0, 3.0, 0]) \nsquare(size=[8, 6], center=true);"
    )
    assert re.left == -8
    assert re.right == 8
    assert re.center_x == 0
    assert re.back == -8
    assert re.front == 8
    assert re.center_y == 0
    assert re.bottom == 0
    assert re.top == 6
    assert re.center_z == 3


def test_slide():
    s = Slide(z=4)(Cube(2, 4, 3))
    assert (
        s.render()
        == "hull() \n{\n  cube(size=[2, 4, 3], center=true);\n  translate(v=[0, 0, 4]) \n  cube(size=[2, 4, 3], center=true);\n}"
    )
    assert s.left == -1
    assert s.right == 1
    assert s.center_x == 0
    assert s.back == -2
    assert s.front == 2
    assert s.center_y == 0
    assert s.bottom == -1.5
    assert s.top == 1.5
    assert s.center_z == 0
