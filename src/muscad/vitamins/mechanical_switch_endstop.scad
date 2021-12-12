union() {
  // endstop_body
  // volume
  cube(size=[14.0, 6.0, 6.0], center=true);
  // switch
  translate(v=[-4.0, -3.5, 0.0])
  // volume
  cube(size=[1.0, 1.0, 6.0], center=true);
  // lever
  rotate(a=[0, 0, 255])
  {
    // volume
    cube(size=[0.5, 13.5, 6.0], center=true);
    difference() {
      cylinder(h=6, d=4, $fn=31, center=true);
      cylinder(h=6.04, d=3, $fn=23, center=true);
      translate(v=[4.5, 0, 0])
      cube(size=[10, 10, 20], center=true);
    }
  }
}
