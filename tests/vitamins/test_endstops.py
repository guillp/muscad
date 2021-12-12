from ..conftest import compare_str
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.endstops import BIQUEndstop
from muscad.vitamins.endstops import InductionSensor
from muscad.vitamins.endstops import MechanicalEndstopOnPCB
from muscad.vitamins.endstops import MechanicalSwitchEndstop
from muscad.vitamins.endstops import OpticalEndstop
from muscad.vitamins.endstops import OptoSwitch


def test_optoswitch():
    compare_str(
        OptoSwitch(),
        """difference() {
  union() {
    // base
    // volume
    cube(size=[24.5, 3.5, 6.4], center=true);
    // left_side
    // volume
    translate(v=[-3.395, 3.9, -0.05])
    cube(size=[4.45, 11.3, 6.3], center=true);
    // right_side
    // volume
    translate(v=[3.395, 3.9, -0.05])
    cube(size=[4.45, 11.3, 6.3], center=true);
  }
  // left_hole
  translate(v=[-9.5, 0, 0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
  // right_hole
  translate(v=[9.5, 0, 0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
}""",
    )


def test_optical_endstop():
    compare_str(
        OpticalEndstop(),
        """difference() {
  union() {
    // base
    color("red")
    // volume
    cube(size=[33.0, 1.6, 10.5], center=true);
    // switch
    color("grey")
    translate(v=[4.15, 2.55, 0])
    difference() {
      union() {
        // base
        // volume
        cube(size=[24.5, 3.5, 6.4], center=true);
        // left_side
        // volume
        translate(v=[-3.395, 3.9, -0.05])
        cube(size=[4.45, 11.3, 6.3], center=true);
        // right_side
        // volume
        translate(v=[3.395, 3.9, -0.05])
        cube(size=[4.45, 11.3, 6.3], center=true);
      }
      // left_hole
      translate(v=[-9.5, 0, 0])
      rotate(a=[270, 0, 180])
      cylinder(h=4.5, d=3, $fn=23, center=true);
      // right_hole
      translate(v=[9.5, 0, 0])
      rotate(a=[270, 0, 180])
      cylinder(h=4.5, d=3, $fn=23, center=true);
    }
    // led
    color("blue")
    // volume
    translate(v=[4.5, 1.15, 0])
    cube(size=[2.0, 0.7, 1.5], center=true);
    // connector
    color("white")
    // volume
    translate(v=[-13.8, -4.3, 0])
    cube(size=[5.8, 7.0, 10.5], center=true);
  }
  // left_hole
  translate(v=[-5.35, 0, 0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
  // right_hole
  translate(v=[13.65, 0, 0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
}""",
    )


def test_biqu_endstop():
    compare_str(
        BIQUEndstop(),
        """union() {
  // body
  linear_extrude(height=1, center=false, convexity=10, twist=0, scale=1.0)
  hull()
  {
    translate(v=[-10.0, 0, 0])
    circle(d=7, $fn=54);
    translate(v=[10.0, 0, 0])
    circle(d=7, $fn=54);
  }
  // endstop
  // volume
  translate(v=[0, 6.5, 3.0])
  cube(size=[13.0, 6.0, 4.0], center=true);
}""",
    )


def test_mechanical_switch_endstop():
    compare_str(
        MechanicalSwitchEndstop(),
        """union() {
  // body
  // volume
  cube(size=[14.0, 6.0, 6.0], center=true);
  // switch
  translate(v=[-4.0, 3.5, 0])
  // volume
  cube(size=[1.0, 1.0, 6.0], center=true);
  // lever
  translate(v=[-7.0, 3.0, 0])
  rotate(a=[0, 0, 15])
  translate(v=[13.5, 0, 0])
  {
    translate(v=[-6.75, 0.25, 0])
    // volume
    cube(size=[13.5, 0.5, 6.0], center=true);
    translate(v=[1.5, -0.5, 0])
    intersection() {
      translate(v=[0, 5.5, 0])
      cube(size=[10, 10, 20], center=true);
      difference() {
        cylinder(h=6, d=4, $fn=31, center=true);
        cylinder(h=7, d=3, $fn=23, center=true);
      }
    }
  }
}""",
    )


def test_induction_sensor():
    compare_str(
        InductionSensor.LJ12A3(),
        """// sensor
cylinder(h=60, d=12.4, $fn=97, center=true);""",
    )


def test_mechanical_endstop_on_pcb():
    compare_str(
        MechanicalEndstopOnPCB(Bolt.M3(10)),
        """union() {
  // pcb
  // volume
  cube(size=[40.0, 16.0, 1.6], center=true);
  // switch
  translate(v=[7.0, 5.0, 3.8])
  union() {
    // body
    // volume
    cube(size=[14.0, 6.0, 6.0], center=true);
    // switch
    translate(v=[-4.0, 3.5, 0])
    // volume
    cube(size=[1.0, 1.0, 6.0], center=true);
    // lever
    translate(v=[-7.0, 3.0, 0])
    rotate(a=[0, 0, 15])
    translate(v=[13.5, 0, 0])
    {
      translate(v=[-6.75, 0.25, 0])
      // volume
      cube(size=[13.5, 0.5, 6.0], center=true);
      translate(v=[1.5, -0.5, 0])
      intersection() {
        translate(v=[0, 5.5, 0])
        cube(size=[10, 10, 20], center=true);
        difference() {
          cylinder(h=6, d=4, $fn=31, center=true);
          cylinder(h=7, d=3, $fn=23, center=true);
        }
      }
    }
  }
  // connector
  translate(v=[-15.0, 0, 3.8])
  // volume
  cube(size=[10.0, 10.0, 6.0], center=true);
  // switch_welds
  difference() {
    // volume
    translate(v=[7.0, 0, -1.8])
    cube(size=[14.0, 4.0, 2.0], center=true);
    // front_bottom_chamfer
    translate(v=[-0.02, 1.0, -1.8])
    rotate(a=[0, 90, 0])
    linear_extrude(height=14.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // back_bottom_chamfer
    translate(v=[-0.02, -1.0, -1.8])
    rotate(a=[270, 0, 0])
    rotate(a=[0, 90, 0])
    linear_extrude(height=14.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // bottom_right_chamfer
    translate(v=[13.0, 2.02, -1.8])
    rotate(a=[90, 90, 0])
    linear_extrude(height=4.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // bottom_left_chamfer
    translate(v=[1.0, 2.02, -1.8])
    rotate(a=[90, 180, 0])
    linear_extrude(height=4.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
  }
  // connector_welds
  difference() {
    // volume
    translate(v=[-10.0, 0, -1.8])
    cube(size=[3.0, 10.0, 2.0], center=true);
    // front_bottom_chamfer
    translate(v=[-11.52, 4.0, -1.8])
    rotate(a=[0, 90, 0])
    linear_extrude(height=3.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // back_bottom_chamfer
    translate(v=[-11.52, -4.0, -1.8])
    rotate(a=[270, 0, 0])
    rotate(a=[0, 90, 0])
    linear_extrude(height=3.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // bottom_right_chamfer
    translate(v=[-9.5, 5.02, -1.8])
    rotate(a=[90, 90, 0])
    linear_extrude(height=10.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
    // bottom_left_chamfer
    translate(v=[-10.5, 5.02, -1.8])
    rotate(a=[90, 180, 0])
    linear_extrude(height=10.04, center=false, convexity=10, twist=0, scale=1.0)
    difference() {
      // box
      translate(v=[0.5, 0.5, 0])
      square(size=[1.04, 1.04], center=true);
      // fillet
      circle(d=2, $fn=15);
    }
  }
  // bolts
  union() {
    translate(v=[7.0, 0, 0])
    mirror(v=[1, 0, 0])
    translate(v=[9.5, 5.5, -3.0])
    rotate(a=[180, 0, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=5.9, $fn=46, center=true);
    }
    translate(v=[16.5, 5.5, -3.0])
    rotate(a=[180, 0, 0])
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
