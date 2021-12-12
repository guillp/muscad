difference() {
  union() {
    // base
    color("red")
    // volume
    cube(size=[33.0, 1.6, 10.5], center=true);
    // switch
    color("grey")
    translate(v=[4.15, 2.55, 0.0])
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
      translate(v=[-9.5, 0.0, 0.0])
      rotate(a=[270, 0, 180])
      cylinder(h=4.5, d=3, $fn=23, center=true);
      // right_hole
      translate(v=[9.5, 0.0, 0.0])
      rotate(a=[270, 0, 180])
      cylinder(h=4.5, d=3, $fn=23, center=true);
    }
    // led
    color("blue")
    // volume
    translate(v=[4.5, 1.15, 0.0])
    cube(size=[2.0, 0.7, 1.5], center=true);
    // connector
    color("white")
    // volume
    translate(v=[-13.8, -4.3, 0.0])
    cube(size=[5.8, 7.0, 10.5], center=true);
  }
  // left_hole
  translate(v=[-5.35, 0.0, 0.0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
  // right_hole
  translate(v=[13.65, 0.0, 0.0])
  rotate(a=[270, 0, 180])
  cylinder(h=4.5, d=3, $fn=23, center=true);
}
