from muscad.vitamins.fans import Blower, Fan

from ..conftest import compare_str


def test_blower() -> None:
    compare_str(
        Blower.blower50x50x15(),
        """union() {
  // fan
  cylinder(h=15.4, d=50.4, $fn=395, center=true);
  // bolt_holders
  hull()
  {
    translate(v=[-23.0, -19.0, 0])
    cylinder(h=15.4, d=6.378, $fn=50, center=true);
    translate(v=[19.5, 19.3, 0])
    cylinder(h=15.4, d=6.378, $fn=50, center=true);
  }
  // blower
  // volume
  translate(v=[-17.0, 22.6, 0])
  cube(size=[19.4, 45.2, 15.4], center=true);
  // back_bolt
  translate(v=[-23.0, -19.0, 3.48])
  union() {
    // thread
    cylinder(h=20, d=4.378, $fn=34, center=true);
    // head
    translate(v=[0, 0, -12.08])
    cylinder(h=4.2, d=7.3, $fn=57, center=true);
    translate(v=[0, 0, 7.98])
    // nut
    cylinder(h=4.2, d=7.3, $fn=6, center=true);
    // inline_nut_clearance
    hull()
    {
      translate(v=[0, 0, 7.98])
      // nut
      cylinder(h=4.2, d=7.3, $fn=6, center=true);
      translate(v=[0, 0, 27.98])
      // nut
      cylinder(h=4.2, d=7.3, $fn=6, center=true);
    }
  }
  // front_bolt
  translate(v=[19.5, 19.3, 3.48])
  union() {
    // thread
    cylinder(h=20, d=4.378, $fn=34, center=true);
    // head
    translate(v=[0, 0, -12.08])
    cylinder(h=4.2, d=7.3, $fn=57, center=true);
    translate(v=[0, 0, 7.98])
    // nut
    cylinder(h=4.2, d=7.3, $fn=6, center=true);
    // inline_nut_clearance
    hull()
    {
      translate(v=[0, 0, 7.98])
      // nut
      cylinder(h=4.2, d=7.3, $fn=6, center=true);
      translate(v=[0, 0, 27.98])
      // nut
      cylinder(h=4.2, d=7.3, $fn=6, center=true);
    }
  }
}""",
    )


def test_fan() -> None:
    compare_str(
        Fan.fan40x40x20().add_tunnel(40, 60),
        """union() {
  // body
  difference() {
    // volume
    cube(size=[40.4, 40.4, 20.4], center=true);
    // front_right_chamfer
    translate(v=[18.2, 18.2, -10.22])
    linear_extrude(height=20.44, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2.04, 2.04], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_right_chamfer
    translate(v=[18.2, -18.2, -10.22])
    rotate(a=[0, 0, 270])
    linear_extrude(height=20.44, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2.04, 2.04], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // back_left_chamfer
    translate(v=[-18.2, -18.2, -10.22])
    rotate(a=[0, 0, 180])
    linear_extrude(height=20.44, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2.04, 2.04], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
    // front_left_chamfer
    translate(v=[-18.2, 18.2, -10.22])
    rotate(a=[0, 0, 90])
    linear_extrude(height=20.44, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[1.0, 1.0, 0])
      square(size=[2.04, 2.04], center=true);
      // fillet
      circle(d=4, $fn=31);
    }
  }
  // bolts
  translate(v=[0, 0, 5.08])
  {
    rotate(a=[0, 0, 45])
    translate(v=[22.6274, 0, 0])
    union() {
      // thread
      cylinder(h=25, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -13.88])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
      translate(v=[0, 0, 11.18])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
    rotate(a=[0, 0, 135])
    translate(v=[22.6274, 0, 0])
    union() {
      // thread
      cylinder(h=25, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -13.88])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
      translate(v=[0, 0, 11.18])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
    rotate(a=[0, 0, 225])
    translate(v=[22.6274, 0, 0])
    union() {
      // thread
      cylinder(h=25, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -13.88])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
      translate(v=[0, 0, 11.18])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
    rotate(a=[0, 0, 315])
    translate(v=[22.6274, 0, 0])
    union() {
      // thread
      cylinder(h=25, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -13.88])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
      translate(v=[0, 0, 11.18])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
  }
  // tunnel
  cylinder(h=60, d=40, $fn=314, center=true);
}""",
    )
