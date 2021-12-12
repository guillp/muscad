difference() {
  union() {
    // pcb
    // volume
    cube(size=[40.0, 16.0, 1.6], center=true);
    // switch
    translate(v=[7.0, 5.0, 3.8])
    union() {
      // endstop_body
      // volume
      cube(size=[14.0, 6.0, 6.0], center=true);
      // switch
      translate(v=[-4.0, 3.5, 0.0])
      // volume
      cube(size=[1.0, 1.0, 6.0], center=true);
      // lever
      #translate(v=[-7.0, 3.0, 0])
      rotate(a=[0, 0, 15])
      translate(v=[13.5, 0.0, 0])
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
    translate(v=[-15.0, 0.0, 3.8])
    // volume
    cube(size=[10.0, 10.0, 6.0], center=true);
    // switch_welds
    difference() {
      // volume
      translate(v=[7.0, 0.0, -1.8])
      cube(size=[14.0, 3.0, 2.0], center=true);
      // front_bottom_chamfer
      translate(v=[-0.02, 0.5, -1.8])
      rotate(a=[0, 90, 0])
      linear_extrude(height=14.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // back_bottom_chamfer
      translate(v=[-0.02, -0.5, -1.8])
      rotate(a=[270, 0, 0])
      rotate(a=[0, 90, 0])
      linear_extrude(height=14.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // bottom_right_chamfer
      translate(v=[13.0, 1.52, -1.8])
      rotate(a=[90, 90, 0])
      linear_extrude(height=3.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // bottom_left_chamfer
      translate(v=[1.0, 1.52, -1.8])
      rotate(a=[90, 180, 0])
      linear_extrude(height=3.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
    }
    // connector_welds
    difference() {
      // volume
      translate(v=[-10.0, 0.0, -1.8])
      cube(size=[3.0, 10.0, 2.0], center=true);
      // front_bottom_chamfer
      translate(v=[-11.52, 4.0, -1.8])
      rotate(a=[0, 90, 0])
      linear_extrude(height=3.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // back_bottom_chamfer
      translate(v=[-11.52, -4.0, -1.8])
      rotate(a=[270, 0, 0])
      rotate(a=[0, 90, 0])
      linear_extrude(height=3.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // bottom_right_chamfer
      translate(v=[-9.5, 5.02, -1.8])
      rotate(a=[90, 90, 0])
      linear_extrude(height=10.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
      // bottom_left_chamfer
      translate(v=[-10.5, 5.02, -1.8])
      rotate(a=[90, 180, 0])
      linear_extrude(height=10.04, center=false, convexity=10, twist=0.0, scale=1.0)
      difference() {
        // box
        translate(v=[0.5, 0.5, 0.0])
        square(size=[1.04, 1.04], center=true);
        // fillet
        circle(d=2, $fn=15);
      }
    }
  }
  // bolts
  #union() {
    translate(v=[7.0, 0, 0])
    mirror(v=[1, 0, 0])
    translate(v=[9.5, 5.5, -3.98])
    rotate(a=[180, 0, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=6.8, $fn=53, center=true);
      // head_clearance
      translate(v=[0, 0, -57.76])
      cylinder(h=100, d=6.8, $fn=53, center=true);
      translate(v=[0, 0, 0.7])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
    translate(v=[16.5, 5.5, -3.98])
    rotate(a=[180, 0, 0])
    union() {
      // thread
      cylinder(h=10, d=3.38, $fn=26, center=true);
      // head
      translate(v=[0, 0, -6.38])
      cylinder(h=2.8, d=6.8, $fn=53, center=true);
      // head_clearance
      translate(v=[0, 0, -57.76])
      cylinder(h=100, d=6.8, $fn=53, center=true);
      translate(v=[0, 0, 0.7])
      // nut
      cylinder(h=2.8, d=6.8, $fn=6, center=true);
    }
  }
}
